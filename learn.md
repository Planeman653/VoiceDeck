# Learn.md - Lessons Learned

## PyQt6 API Changes (2024+)

### `currentRowChanged` doesn't exist on QTableWidget
**Error:** `'QTableWidget' object has no attribute 'currentRowChanged'`

**Fix:** Use `selectionModel().currentRowChanged` instead.

**Pattern:**
```python
# WRONG (PyQt6)
self.table.currentChanged.connect(handler)

# WRONG (PyQt5 style)
self.table.currentRowChanged.connect(handler)

# CORRECT (PyQt6)
selection_model = self.table.selectionModel()
selection_model.currentRowChanged.connect(lambda idx: handler(idx.row()))
```

### `QLineEdit.Normal` deprecated
**Error:** `AttributeError: type object 'QLineEdit' has no attribute 'Normal'`

**Fix:** Use `QLineEdit.EchoMode.Normal` or omit the echo parameter (has default).

**Pattern:**
```python
# OLD (PyQt5 / old PyQt6)
QInputDialog.getText(parent, title, label, QLineEdit.Normal, text)

# NEW (current PyQt6)
QInputDialog.getText(parent, title, label, QLineEdit.EchoMode.Normal, text)

# Or omit echo:
QInputDialog.getText(parent, title, label, text)
```

### `QInputDialog.getText()` return order changed
**Error:** `TypeError: ... argument 4 has unexpected type 'str'`

**Fix:** PyQt6 returns `(text, ok)` not `(ok, text)`.

**Pattern:**
```python
# OLD (PyQt5)
ok, text = QInputDialog.getText(parent, title, label, echo, text)

# NEW (PyQt6)
text, ok = QInputDialog.getText(parent, title, label, echo, text)
```

## SoundDevice Fallback Pattern

### When external audio library fails to import
**Error:** `ModuleNotFoundError: No module named 'sounddevice'`

**Fix:** Use try/except to gracefully fall back to system beep:

```python
try:
    import sounddevice as sd
    import soundfile as sf
    USE_SOUNDDEVICE = True
except ImportError:
    USE_SOUNDDEVICE = False
```

This ensures the app works even when optional audio libraries aren't installed.

## Audio Device Selection

### Output and Input Device Configuration

**Feature:** Added device selection in Settings > Audio Devices section.

**Usage:**
1. Go to Settings tab
2. See list of available output devices (speakers/headphones)
3. See list of available input devices (microphones)
4. Select your preferred devices
5. Click "Save Settings"

**Output devices** will play your audio (speakers, headphones)

**Input devices** are used for microphone listening (VoiceDeck voice triggers)

### Config Keys Added
- `"output_device_index"` - Index of output device (null for default)
- `"input_device_index"` - Index of input device (null for default)

**Files modified:**
- `audio_manager/audio_player.py` - Added device initialization and selection
- `ui/settings_page.py` - Added device selection UI and handlers
- `main.py` - Pass device settings to AudioPlayer
- `requirements.txt` - Added sounddevice, soundfile, scipy

## Audio Playback Issue

### sounddevice as primary audio library
**Status:** Now installed and working.

**Install:**
```bash
pip install sounddevice soundfile scipy
```

**Fallback:** If sounddevice isn't available, the app uses `winsound.Beep()` as a fallback.

**Updated:** `audio_manager/audio_player.py` now uses `sounddevice` with graceful fallback.

### Troubleshooting No Sound
If sound doesn't play:
1. Check device selection in Settings > Audio Devices
2. Select your speakers/headphones in Output Device dropdown
3. Select your microphone in Input Device dropdown
4. Save settings and restart the app
5. Ensure Windows volume is not muted
6. Check that audio devices are enabled in Windows Sound settings

## `QSystemTrayIcon` warning

**Warning:** `QSystemTrayIcon::setVisible: No Icon set`

This is a harmless warning when the tray icon is created before an application icon is set. The application still works correctly.

## Notes

This file tracks lessons learned and patterns to avoid during development.
