"""Audio player for playback control"""
import pygame
from pathlib import Path


class AudioPlayer:
    """Handles audio file playback"""

    def __init__(self, volume: float = 1.0, audio_folder: Path | None = None):
        """Initialize audio player

        Args:
            volume: Initial volume level (0.0 to 1.0)
            audio_folder: Folder containing audio files
        """
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()

        self.audio_folder = Path(audio_folder) if audio_folder else None
        self.volume = volume
        self._current_volume = volume

    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 = silent, 1.0 = normal)"""
        self._current_volume = max(0.0, min(1.0, volume))
        pygame.mixer.set_volume(int(self._current_volume * 100))

    def play(self, file_path: Path | str, volume: float | None = None) -> bool:
        """Play an audio file

        Args:
            file_path: Path to audio file
            volume: Optional volume override for this playback

        Returns:
            True if playback started successfully
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        try:
            # Use custom volume if specified, otherwise use default
            vol = volume if volume is not None else self._current_volume
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(volume=vol)
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False

    def stop(self) -> None:
        """Stop currently playing audio"""
        pygame.mixer.music.stop()

    def pause(self) -> None:
        """Pause current playback"""
        pygame.mixer.music.pause()

    def resume(self) -> None:
        """Resume paused playback"""
        pygame.mixer.music.unpause()

    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        return pygame.mixer.music.get_busy()

    def seek(self, position: float) -> None:
        """Seek to position (seconds)"""
        pygame.mixer.music.set_pos(position)

    def fade_in(self, duration_ms: int = 500) -> None:
        """Fade in from silence"""
        try:
            pygame.mixer.music.set_fadein(duration_ms / 1000.0)
        except Exception:
            pass

    def fade_out(self, duration_ms: int = 500) -> None:
        """Fade out to silence"""
        try:
            pygame.mixer.music.set_fadeout(duration_ms / 1000.0)
        except Exception:
            pass
