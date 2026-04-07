# VoiceDeck

A voice-activated audio player for Windows that uses local AI to recognize voice triggers and play corresponding audio files.

## Features

- **Voice Activation**: Say trigger phrases to play audio files
- **Local AI**: Uses Whisper (tiny model) for offline speech recognition
- **Configurable Sensitivity**: Adjust AI sensitivity from exact match to fuzzy matching
- **Sequential Playback**: Queue up audio files automatically
- **Simple UI**: Clean, modern interface with media controls
- **Tray Icon**: Minimize to system tray

## Installation

1. **Clone or download** this repository
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**:
   ```bash
   python main.py
   ```

The app will auto-download the Whisper model (~75MB) on first run.

## Usage

1. **Launch the app**: `python main.py`

2. **Add audio files**:
   - Click "Upload MP3" or drag MP3 files into the app folder
   - Set trigger phrases for each file (auto-detected from filename)

3. **Configure AI**:
   - Go to Settings tab
   - Adjust sensitivity (0-100)
   - Select AI model size
   - Enable/disable microphone listening

4. **Use voice commands**:
   - Toggle microphone listening
   - Say your trigger phrases
   - App will play matching audio files

## Project Structure

```
VoiceDeck/
├── main.py              # Application entry point
├── tray.py              # System tray icon
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── LICENSE              # MIT License
├── ai_engine/           # AI and speech recognition
│   ├── __init__.py
│   ├── whisper_transcriber.py    # Whisper STT integration
│   ├── trigger_classifier.py     # Trigger phrase matching
│   └── audio_streamer.py         # Microphone audio stream
├── audio_manager/       # Audio playback
│   ├── __init__.py
│   ├── audio_player.py  # Audio playback control (winsound)
│   └── audio_queue.py   # Queue management
├── ui/                  # PyQt6 UI components
│   ├── __init__.py
│   ├── main_window.py   # Main window
│   ├── media_bar.py     # Media controls
│   ├── audio_list_page.py   # Library tab
│   ├── settings_page.py  # Settings tab
│   └── upload_dialog.py  # Upload dialog
├── models/              # Data models
│   ├── trigger_entry.py
│   └── app_config.py
└── config/              # Configuration
    └── default_settings.json
```

## Testing

Verify imports work:
```bash
python -c "from ai_engine import WhisperTranscriber, TriggerClassifier; print('OK')"
```

## AI Model

- **Default**: `tiny` (~75MB, fast but less accurate)
- **Options**: `base`, `small`, `medium`, `large`
- Larger models are more accurate but require more RAM

## Sensitivity Settings

- **0-30**: Exact phrase match required
- **30-70**: Partial matches accepted
- **70-100**: Very loose matching (substring, similar context)

## Requirements

- Python 3.8+
- Windows 10/11
- Internet connection for first-time model download
- Microphone (for voice activation)
- Speakers (for audio output)

## Note on Audio Playback

This app uses Windows built-in `winsound` for notifications. For full MP3 playback:
- Configure your system to use a media player for audio files
- The app uses beep notifications to indicate tracks are queued

To implement full audio playback, you can integrate with Windows Media Player or similar.

## Creating an Executable

To create a standalone executable:
```bash
pip install pyinstaller
pyinstaller --windowed --name VoiceDeck main.py
```

## License

MIT License - See LICENSE file
