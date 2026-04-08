"""Whisper-based speech-to-text transcriber"""
import threading
from pathlib import Path


class WhisperTranscriber:
    """Handles speech-to-text transcription using Whisper"""

    MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]

    def __init__(self, model_name: str = "tiny", device: str = None):
        """Initialize Whisper transcriber

        Args:
            model_name: Size of Whisper model to load
            device: Device to run inference on (cpu/cuda)
        """
        self.model_name = model_name
        # Try to detect CUDA, fall back to CPU if torch not available
        try:
            import torch
            self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        except ImportError:
            self.device = device or "cpu"
        self.model = None
        self._loaded = False
        self._lock = threading.Lock()
        self._load_model()

    def _load_model(self) -> None:
        """Load Whisper model in a thread"""
        def load():
            try:
                import whisper
                self.model = whisper.load_model(
                    self.model_name,
                    device=self.device
                )
            except ImportError as e:
                print(f"Whisper not installed: {e}")
        threading.Thread(target=load, daemon=True).start()

    def transcribe(self, audio_path: Path | bytes | str, language: str = None) -> dict:
        """Transcribe audio to text

        Args:
            audio_path: Path to audio file or audio bytes
            language: Optional language code (e.g., 'en', 'es')

        Returns:
            Dict with 'text' and 'chunks' containing transcribed text segments
        """
        if not self.model:
            self._load_model()

        import whisper
        if hasattr(self.model, 'device') and self.model.device != self.device:
            self.model = whisper.load_model(self.model_name, device=self.device)

        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            temperature=0.0 if language else 0.7
        )

        text = result.get("text", "").strip()
        chunks = result.get("segments", [])

        return {
            "text": text,
            "chunks": chunks,
            "language": result.get("language", language or "unknown")
        }

    def transcribe_stream(self, audio_data: bytes, duration: int = None) -> list:
        """Transcribe audio stream in chunks

        Args:
            audio_data: Audio data as bytes
            duration: Optional duration threshold (in seconds) for chunking

        Returns:
            List of transcribed text chunks
        """
        import whisper
        if not self.model:
            self._load_model()

        if hasattr(self.model, 'device') and self.model.device != self.device:
            self.model = whisper.load_model(self.model_name, device=self.device)

        # Save to temp file and transcribe
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_data)
            temp_path = f.name

        # For simplicity, transcribe as one segment
        result = self.model.transcribe(temp_path)
        text = result.get("text", "")
        chunks = result.get("segments", [])

        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)

        return [c["text"].strip() for c in chunks] if chunks else [text]

    def get_model_info(self) -> dict:
        """Get model information"""
        try:
            import torch
            has_cuda = torch.cuda.is_available() if self.device == "cuda" else False
        except ImportError:
            has_cuda = False
        return {
            "model_name": self.model_name,
            "device": self.device,
            "has_cuda": has_cuda
        }