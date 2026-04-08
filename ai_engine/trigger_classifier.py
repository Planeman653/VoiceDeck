"""Trigger classifier for matching speech to audio triggers"""
import re
from typing import List, Optional


class TriggerClassifier:
    MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]
    """
    Classifies transcribed speech against registered trigger phrases.
    Uses configurable sensitivity for fuzzy matching.
    """

    def __init__(self, transcriber=None):
        """Initialize trigger classifier

        Args:
            transcriber: WhisperTranscriber instance
        """
        self.transcriber = transcriber
        self.sensitivity = 0.5  # 0.0 (exact) to 1.0 (very loose)
        self.triggers = {}  # filename -> trigger_phrase mapping
        self.last_transcription = ""

    def set_sensitivity(self, value: float) -> None:
        """Set sensitivity (0.0 = exact match, 1.0 = very loose)"""
        self.sensitivity = max(0.0, min(1.0, value))

    def add_trigger(self, filename: str, trigger_phrase: str = None) -> None:
        """Register a trigger phrase for an audio file

        Args:
            filename: Audio file name (without extension)
            trigger_phrase: Phrase to trigger playback. If None, auto-generate from filename
        """
        # Generate trigger from filename if not provided
        if trigger_phrase is None:
            clean_name = filename.replace(".mp3", "").replace("_", " ").replace("-", " ")
            trigger_phrase = clean_name.strip()

        self.triggers[filename] = {
            "trigger_phrase": trigger_phrase,
            "description": trigger_phrase,
            "enabled": True
        }

    def remove_trigger(self, filename: str) -> None:
        """Remove a trigger registration"""
        if filename in self.triggers:
            del self.triggers[filename]

    def get_all_triggers(self) -> dict:
        """Get all registered triggers"""
        return {name: info for name, info in self.triggers.items() if info["enabled"]}

    def get_triggers_for_text(self, text: str) -> List[str]:
        """
        Get list of trigger filenames that match the given text
        based on current sensitivity level.

        Args:
            text: Transcribed speech text

        Returns:
            List of filenames for matching triggers
        """
        if not text:
            return []

        # Normalize text for matching
        normalized = text.lower().strip()

        matches = []
        for filename, info in self.triggers.items():
            trigger = info["trigger_phrase"]

            # Skip disabled triggers
            if not info.get("enabled", True):
                continue

            # Get trigger phrases to check (include variations based on sensitivity)
            trigger_phrases = self._get_trigger_variations(trigger, info)

            if any(normalized == t for t in trigger_phrases):
                matches.append(filename)
            elif self.sensitivity > 0:
                # Fuzzy matching based on sensitivity
                if self._fuzzy_match(normalized, trigger, info):
                    matches.append(filename)

        return matches

    def _get_trigger_variations(self, trigger: str, info: dict) -> List[str]:
        """Get variations of trigger phrase for matching"""
        variations = [trigger.lower()]

        # Word-level variations
        words = trigger.lower().split()
        for i in range(1, len(words) + 1):
            for start in range(len(words)):
                for length in range(1, len(words) - start + 1):
                    variations.append(" ".join(words[start:start + length]))

        # Handle punctuation removal
        trigger_no_punct = re.sub(r'[^\w\s]', '', trigger)
        variations.append(trigger_no_punct.lower())

        return variations

    def _fuzzy_match(self, text: str, trigger: str, info: dict) -> bool:
        """
        Perform fuzzy matching based on sensitivity.

        Args:
            text: Normalized transcribed text
            trigger: Original trigger phrase
            info: Trigger information dict

        Returns:
            True if text matches trigger within sensitivity threshold
        """
        text_words = set(text.split())
        trigger_words = set(trigger.split())

        if not trigger_words:
            return False

        # Calculate overlap ratio
        common_words = text_words.intersection(trigger_words)
        if not common_words:
            return False

        # Simple word overlap ratio
        overlap_ratio = len(common_words) / len(trigger_words)

        # At higher sensitivity, accept lower overlap
        min_threshold = 0.3 if self.sensitivity > 0.8 else 0.6

        return overlap_ratio >= min_threshold

    def classify(self, audio_path: str, language: str = None) -> dict:
        """
        Classify audio to determine if any triggers should fire.

        Args:
            audio_path: Path to audio file
            language: Optional language code

        Returns:
            Dict with 'matches' (list of trigger filenames) and 'text'
        """
        if not self.transcriber:
            return {"matches": [], "text": "", "confidence": 0.0}

        # Transcribe audio
        result = self.transcriber.transcribe(audio_path, language=language)
        text = result.get("text", "")

        # Classify
        matches = self.get_triggers_for_text(text)

        return {
            "matches": matches,
            "text": text,
            "language": result.get("language", language or "unknown"),
            "chunks": result.get("chunks", [])
        }

    def reset(self) -> None:
        """Clear last transcription"""
        self.last_transcription = ""
