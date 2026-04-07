"""Audio stream processor for real-time trigger detection"""
import pyaudio
import numpy as np
import threading
import queue
from typing import Callable, Optional
from pathlib import Path


class AudioStreamer:
    """
    Real-time microphone audio stream processor.
    Buffers audio chunks and triggers classification periodically.
    """

    CHUNK_SIZE = 1024  # Samples per chunk (10ms at 44.1kHz)
    SAMPLING_RATE = 44100

    def __init__(
        self,
        classifier,
        on_match: Callable = None,
        sensitivity: float = 0.5
    ):
        """Initialize audio streamer

        Args:
            classifier: TriggerClassifier instance
            on_match: Callback when trigger is matched
            sensitivity: AI sensitivity (0.0 to 1.0)
        """
        self.classifier = classifier
        self.on_match = on_match
        self.sensitivity = sensitivity
        self.microphone = None
        self.stream = None
        self._running = False
        self._thread = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start microphone listening"""
        # Initialize PyAudio
        self.microphone = pyaudio.PyAudio()
        self.stream = self.microphone.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.CHUNK_SIZE
        )

        self._running = True
        self._thread = threading.Thread(target=self._process_audio, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop microphone listening"""
        self._running = False
        self._stop_event.set()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.microphone:
            self.microphone.terminate()

    def _process_audio(self) -> None:
        """Main audio processing loop"""
        buffer = np.zeros(self.CHUNK_SIZE, dtype=np.float32)
        silence_threshold = 0.01  # RMS threshold for silence detection

        while self._running:
            try:
                data = self.stream.read(
                    self.CHUNK_SIZE,
                    exception_on_overflow=False
                )

                # Convert to float
                samples = np.frombuffer(data, dtype=np.int16)
                samples = samples.astype(np.float32) / 32768.0

                # Check for silence
                rms = np.sqrt(np.mean(samples ** 2))
                if rms < silence_threshold:
                    continue

                # Accumulate audio for transcription
                # For simplicity, we'll do periodic transcription
                buffer = np.concatenate([buffer, samples])

                # Transcribe every 5 seconds (approx 250 chunks)
                if len(buffer) >= self.CHUNK_SIZE * 250:
                    self._transcribe_buffer(buffer)
                    buffer = buffer[:self.CHUNK_SIZE]  # Keep first chunk

            except Exception as e:
                print(f"Audio error: {e}")

    def _transcribe_buffer(self, audio_data: np.ndarray) -> None:
        """Transcribe audio buffer and classify"""
        try:
            # Convert numpy array to bytes
            audio_bytes = (audio_data * 32768.0).astype(np.int16).tobytes()

            # Classify
            result = self.classifier.classify(
                audio_path=audio_bytes,
                language=None
            )

            matches = result.get("matches", [])
            if matches:
                for match in matches:
                    if self.on_match:
                        self.on_match(match)
            else:
                self.classifier.reset()

        except Exception as e:
            print(f"Transcription error: {e}")

    def set_sensitivity(self, sensitivity: float) -> None:
        """Set AI sensitivity"""
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        self.classifier.set_sensitivity(sensitivity)

    @property
    def is_running(self) -> bool:
        """Check if streamer is running"""
        return self._running
