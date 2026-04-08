"""
VoiceDeck - Voice-Activated Audio Player
Main application entry point
"""
import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add parent directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def main():
    from ai_engine import WhisperTranscriber, TriggerClassifier
    AudioStreamer = None  # Will be imported if available
    from audio_manager import AudioPlayer, AudioQueue
    from ui import MainWindow

    # Ensure directories exist
    config_dir = SCRIPT_DIR / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Default settings
    config_file = config_dir / "default_settings.json"
    if not config_file.exists():
        config_file.write_text("""{
    "audio_folder": "resources/audio",
    "default_volume": 1.0,
    "ai_model": "tiny",
    "sensitivity": 50,
    "enable_listening": true,
    "language": "en"
}""")

    # Load config
    with open(config_file) as f:
        config = json.load(f)

    # Initialize audio player
    audio_player = AudioPlayer(
        volume=config["default_volume"],
        audio_folder=Path(config["audio_folder"])
    )

    # Initialize audio queue
    audio_queue = AudioQueue(audio_player)

    # Initialize AI engine
    whisper_model_name = config.get("ai_model", "tiny")
    whisper_transcriber = WhisperTranscriber(model_name=whisper_model_name)
    trigger_classifier = TriggerClassifier(transcriber=whisper_transcriber)
    trigger_classifier.set_sensitivity(config.get("sensitivity", 50) / 100.0)

    # Create audio streamer for microphone (if pyaudio is available)
    if AudioStreamer:
        audio_streamer = AudioStreamer(
            classifier=trigger_classifier,
            on_match=audio_queue.play,
            sensitivity=config.get("sensitivity", 50) / 100.0
        )

    # Initialize UI
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Create main window
    main_window = MainWindow(
        trigger_classifier=trigger_classifier,
        audio_queue=audio_queue,
        config=config
    )

    # Set window properties
    main_window.setWindowTitle("VoiceDeck - Voice Activated Audio Player")
    main_window.setMinimumSize(600, 400)

    # Setup microphone listening if enabled and streamer is available
    if config.get("enable_listening", True) and audio_streamer:
        audio_streamer.start()

    # Setup tray (simple hide/show)
    from tray import SimpleTray
    tray = SimpleTray(app, main_window)

    # Set window properties
    main_window.show()
    main_window.raise_()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
