"""AI Engine package - Speech recognition and trigger matching"""
from .whisper_transcriber import WhisperTranscriber
from .trigger_classifier import TriggerClassifier

# Optional audio streamer (requires pyaudio)
try:
    from .audio_streamer import AudioStreamer
except ImportError:
    AudioStreamer = None

__all__ = ["WhisperTranscriber", "TriggerClassifier", "AudioStreamer"]
