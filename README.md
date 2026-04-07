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
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Download Whisper model** (first run will auto-download):
   - The app will download a ~75MB "tiny" model automatically
   - For better accuracy, use `small` (~140MB) or `base` (~140MB) in Settings

## Usage

1. **Launch the app**:
   ```bash
   python main.py
   ```
   Or create a shortcut: `python main.py --window-mode`

2. **Add audio files**:
   - Click "Upload MP3" or drag MP3 files into the app folder
   - Set trigger phrases for each file
   - The trigger is auto-detected from the filename

3. **Configure AI**:
   - Go to Settings tab
   - Adjust sensitivity (0-100)
   - Select AI model size
   - Enable/disable microphone listening

4. **Use voice commands**:
   - Click microphone toggle in Settings
   - Say your trigger phrases
   - App will play matching audio files

2. **Add audio files**:
   - Click "Upload MP3" or drag MP3 files into the app folder
   - Set trigger phrases for each file
   - The trigger is auto-detected from the filename

3. **Configure AI**:
   - Go to Settings tab
   - Adjust sensitivity (0-100)
   - Select AI model size
   - Enable/disable microphone listening

4. **Use voice commands**:
   - Click microphone toggle in Settings
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
│   ├── audio_player.py  # Audio playback control
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

Run the following to test imports (you'll need to install dependencies first):
```bash
pip install -r requirements.txt
python -c "import sys; sys.path.insert(0, '.'); from ai_engine import WhisperTranscriber, TriggerClassifier; print('Imports OK')"
```

The app will auto-download the Whisper model (~75MB) on first run.

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
- Microphone (for voice activation)
- Speakers (for audio output)

## Creating an Executable

To create a standalone executable:
```bash
pip install pyinstaller
pyinstaller --windowed --name VoiceDeck --icon=app.ico main.py
```

## Tray Icon

The app uses a simple tray icon. You can customize it by:
1. Placing an icon file in `assets/icons/app.ico`
2. Modifying `_create_icon()` in `tray.py`

## License

MIT License - See LICENSE file

## Troubleshooting

- **Whisper not found**: Run `pip install -r requirements.txt`
- **Microphone not working**: Check Windows privacy settings
- **Audio distortion**: Reduce volume or upgrade audio hardware
- **Model too large**: Consider using smaller models for limited storage
- **No triggers matching**: Check sensitivity slider (0=exact, 100=loose)
- **Audio doesn't play**: Check output device and app volume
- **UI looks different**: Ensure PyQt6 is properly installed

## Additional Notes

- The app requires a working internet connection for first-time model download
- The tiny Whisper model takes ~75MB; larger models take more space
- Windows 10/11 only - tested on Windows 11
- MP3 files only (other formats not supported)
