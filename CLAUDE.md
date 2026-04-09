# VoiceDeck - Voice-Activated Audio Player

## Commands

## On Every Run
Please check the ./MISTAKES.md file for mistakes that you have made. Keep these in mind moving forward so that you do not make the same mistakes again. If a mistake with your own work is identified, please place that in the mistakes.md file.

### Run the app
```bash
python main.py
```

### Run a single test
```bash
# Test AI engine imports
python -c "from ai_engine import WhisperTranscriber, TriggerClassifier; print('OK')"

# Test audio player
python -c "from audio_manager import AudioPlayer, AudioQueue; print('OK')"

# Test UI
python -c "from ui import MainWindow, MediaBar, SettingsPage; print('OK')"
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Architecture

### Core Flow

```
User speaks → Microphone → AudioStreamer → Whisper Transcriber → TriggerClassifier → Play Audio
```

### Components

#### ai_engine/
- **whisper_transcriber.py**: Loads Whisper model, transcribes audio to text
- **trigger_classifier.py**: Matches transcribed text against registered trigger phrases
- **audio_streamer.py**: Real-time microphone audio processing with periodic transcription

#### audio_manager/
- **audio_player.py**: Uses pygame.mixer for audio playback
- **audio_queue.py**: Manages sequential playback queue

#### ui/
- **main_window.py**: Main PyQt6 window with QTabWidget
- **media_bar.py**: Persistent media controls (play/pause, volume, track info)
- **audio_list_page.py**: Library tab showing all MP3 files with trigger settings
- **settings_page.py**: Settings tab with sensitivity slider, AI model selection
- **upload_dialog.py**: File upload dialog

#### models/
- **trigger_entry.py**: Data model for audio file with trigger mapping
- **app_config.py**: Application configuration management

## Key Patterns

### Sensitivity System
- Slider 0-100 mapped to confidence threshold
- 0 = exact phrase match
- 100 = fuzzy matching (substring, partial phrases)

### Trigger Registration
```python
classifier.add_trigger("joke.mp3", trigger_phrase="tell me a joke")
```

### Playback Control
```python
player.play("audio/file.mp3", volume=0.8)
player.stop()
player.pause()
```

### UI Updates
```python
media_bar.set_track("current_track.mp3")
media_bar.play()
media_bar.set_volume(75)
```

## Testing

### Import all modules
```bash
python -c "
from ai_engine import WhisperTranscriber, TriggerClassifier
from audio_manager import AudioPlayer, AudioQueue
from ui import MainWindow, MediaBar, SettingsPage
print('All imports OK')
"
```

## Notes

- First run will auto-download Whisper tiny model (~75MB)
- Default audio folder: `resources/audio/`
- Sensitivity defaults to 50 (medium)
- Language defaults to English (en)
