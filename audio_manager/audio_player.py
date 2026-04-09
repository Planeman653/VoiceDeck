"""Audio player for playback control using sounddevice"""
try:
    import sounddevice as sd
    import soundfile as sf
    USE_SOUNDDEVICE = True
except ImportError:
    USE_SOUNDDEVICE = False
import winsound
from pathlib import Path
from typing import Optional


class AudioPlayer:
    """
    Handles audio playback using sounddevice or winsound fallback.
    Provides cross-platform audio playback support with device selection.
    """

    def __init__(self, volume: float = 1.0, audio_folder=None,
                 output_device: int = None, input_device: int = None,
                 output_rate: int = 44100):
        """Initialize audio player

        Args:
            volume: Initial volume (0.0 to 1.0)
            audio_folder: Path to audio files folder
            output_device: Index of output device (None = default)
            input_device: Index of input device (None = default)
            output_rate: Sample rate for playback (default: 44100)
        """
        self.audio_folder = Path(audio_folder) if audio_folder else None
        self.volume = volume
        self._current_volume = volume
        self._playing = False
        self._current_track = None
        self._stream = None

        # Store device settings
        self.output_device = output_device
        self.input_device = input_device
        self.output_rate = output_rate

        # Initialize sounddevice mixer if available
        if USE_SOUNDDEVICE:
            try:
                sd.default.samplerate = self.output_rate
                # Get devices and set defaults if not specified
                devices = sd.query_devices()
                if self.output_device is None:
                    # Find an output device
                    out_indices = [i for i, d in enumerate(devices)
                                   if d['max_output_channels'] is not None]
                    self.output_device = out_indices[0] if out_indices else None
                if self.input_device is None:
                    # Find an input device
                    in_indices = [i for i, d in enumerate(devices)
                                 if d['max_input_channels'] is not None]
                    self.input_device = in_indices[0] if in_indices else None
                # Initialize mixer with default devices
                sd.default.device = (self.input_device, self.output_device)
                print(f"Audio initialized: Input={self.input_device}, "
                      f"Output={self.output_device}")
            except Exception as e:
                print(f"Warning: Could not initialize audio device: {e}")
                print("Using system default devices")

    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self._current_volume = max(0.0, min(1.0, volume))
        self.volume = volume

    def play(self, file_path: Path | str, volume: float | None = None) -> bool:
        """
        Play an audio file.

        Args:
            file_path: Path to audio file (MP3, WAV, etc.)
            volume: Optional volume override (0.0 to 1.0)

        Returns:
            True if playback started successfully
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        # Determine actual volume
        actual_volume = volume if volume is not None else self._current_volume

        try:
            # Stop any currently playing stream
            if self._stream is not None:
                self.stop()

            if USE_SOUNDDEVICE:
                # Read audio file
                data, sr = sf.read(str(path))

                # Ensure stereo
                if data.ndim == 1:
                    data = data[:, None]

                # Apply volume
                data = data * actual_volume

                # Create stream
                self._stream = sd.OutputStream(samplerate=sr, channels=data.shape[1])
                self._stream.start()

                # Queue audio for playback
                sd.play(data, samplerate=sr, blocking=False)

                self._playing = True
                self._current_track = str(path)

                return True
            else:
                # Fallback to winsound (beep only)
                import winsound
                winsound.Beep(880, 300)
                self._playing = True
                self._current_track = str(path)
                return True

        except sd.InputStreamError as e:
            print(f"Stream error: {e}")
            return False
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False

    def stop(self) -> None:
        """Stop current playback"""
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            except Exception:
                pass
        self._playing = False
        self._current_track = None

    def pause(self) -> None:
        """Pause current playback"""
        if self._stream is not None:
            try:
                self._stream.stop()
            except Exception:
                pass
        self._playing = False

    def resume(self) -> None:
        """Resume playback"""
        # sounddevice doesn't support pause/resume natively
        # The stream continues playing if not stopped
        pass

    def is_playing(self) -> bool:
        """Check if audio is playing"""
        return self._stream is not None and self._stream.get_state() != 'stopped'

    def is_paused(self) -> bool:
        """Check if playback is paused/stopped"""
        if self._stream is None:
            return False
        state = self._stream.get_state()
        return state in ['stopped', 'finished']

    def seek(self, position: float) -> None:
        """Seek to position (0.0 to 1.0) - restart from position"""
        if self._stream is None or self._current_track is None:
            return
        path = Path(self._current_track)
        if not path.exists():
            return
        data, sr = sf.read(str(path))
        if data.ndim == 1:
            data = data[:, None]
        total_samples = data.shape[0]
        seek_samples = int(total_samples * position)
        # Restart with truncated audio
        data = data[seek_samples:]
        sd.play(data, samplerate=sr, blocking=False)

    def fade_in(self, duration_ms: int = 500) -> None:
        """Fade in (not natively supported by sounddevice)"""
        pass

    def fade_out(self, duration_ms: int = 500) -> None:
        """Fade out (not natively supported by sounddevice)"""
        pass

    def get_stream_info(self) -> dict:
        """Get playback info"""
        return {
            "playing": self._playing,
            "track": self._current_track
        }

    def get_devices(self) -> list:
        """Get list of available audio devices"""
        if not USE_SOUNDDEVICE:
            return []
        try:
            devices = sd.query_devices()
            # Format devices for display
            formatted = []
            for i, dev in enumerate(devices):
                name = dev['name']
                in_ch = dev.get('max_input_channels', 0)
                out_ch = dev.get('max_output_channels', 0)
                if in_ch == 0 and out_ch == 0:
                    type_str = "Input"
                elif in_ch > 0 and out_ch == 0:
                    type_str = "Input"
                elif in_ch == 0 and out_ch > 0:
                    type_str = "Output"
                else:
                    type_str = "Input/Output"
                formatted.append({
                    "index": i,
                    "name": name,
                    "type": type_str
                })
            return formatted
        except Exception as e:
            print(f"Error querying devices: {e}")
            return []

    def set_device(self, device_type: str, device_index: int) -> None:
        """Set output or input device

        Args:
            device_type: 'output' or 'input'
            device_index: Index of device to use
        """
        if not USE_SOUNDDEVICE:
            return
        try:
            if device_type == "output":
                self.output_device = device_index
            elif device_type == "input":
                self.input_device = device_index
            # Apply new device settings
            devices = sd.query_devices()
            out_idx = [i for i, d in enumerate(devices)
                       if d['max_output_channels'] is not None]
            in_idx = [i for i, d in enumerate(devices)
                       if d['max_input_channels'] is not None]
            out_dev = self.output_device if self.output_device is not None else (out_idx[0] if out_idx else None)
            in_dev = self.input_device if self.input_device is not None else (in_idx[0] if in_idx else None)
            sd.default.device = (in_dev, out_dev)
            print(f"Device set: Input={in_dev}, Output={out_dev}")
        except Exception as e:
            print(f"Error setting device: {e}")

    def cleanup(self) -> None:
        """Clean up stream resources"""
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
        self._stream = None
