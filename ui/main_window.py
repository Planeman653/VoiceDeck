"""Main application window with tabs"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


from .media_bar import MediaBar
from .audio_list_page import AudioListPage
from .settings_page import SettingsPage
from .upload_dialog import UploadDialog


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, trigger_classifier, audio_queue, config):
        super().__init__()
        self.trigger_classifier = trigger_classifier
        self.audio_queue = audio_queue
        self.config = config
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the main window UI"""
        self.setWindowTitle("VoiceDeck - Voice Activated Audio Player")
        self.setMinimumSize(600, 400)

        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Media bar at top (persistent)
        self.media_bar = MediaBar()
        self.media_bar.setStyleSheet("""
            MediaBar {
                background-color: #1a1a2e;
                border-bottom: 2px solid #16213e;
            }
            QPushButton {
                background-color: #4a4a6a;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a7a;
            }
        """)
        main_layout.addWidget(self.media_bar)

        # Tab widget for main content
        self.tabs = QTabWidget()
        self.tabs.tabBar().setFixedHeight(40)

        # Audio list tab (library)
        self.audio_page = AudioListPage(self.trigger_classifier, self.audio_queue)
        self.tabs.addTab(self.audio_page, "Library")
        self.tabs.setTabToolTip(0, "Ctrl+1")


        # Settings tab
        self.settings_page = SettingsPage(
            self.trigger_classifier,
            self.config
        )
        self.tabs.addTab(self.settings_page, "Settings")
        self.tabs.setTabToolTip(1, "Ctrl+2")

        # Upload button
        self.upload_btn = QPushButton("Upload MP3")
        self.upload_btn.setFixedHeight(40)
        self.upload_btn.clicked.connect(self._on_upload)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d4aa;
                color: #1a1a2e;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #00e5bb;
            }
            QPushButton:pressed {
                background-color: #00b899;
            }
        """)

        # Tab bar layout
        tab_bar_layout = QHBoxLayout()
        tab_bar_layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignRight)
        tab_bar_layout.addWidget(self.tabs, stretch=1)

        main_layout.addLayout(tab_bar_layout)

        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #16213e;
                color: #aaa;
                padding: 4px;
            }
        """)
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_bar)

    def setup_microphone(self, sensitivity: float) -> None:
        """
        Setup microphone listening.

        Args:
            sensitivity: AI sensitivity (0.0 to 1.0)
        """
        # Placeholder - actual implementation would use pyaudio
        self.status_bar.setText(f"Listening enabled (sensitivity: {sensitivity:.2f})")

    def _on_upload(self) -> None:
        """Handle upload button click"""
        dialog = UploadDialog(
            self,
            trigger_classifier=self.trigger_classifier,
            audio_queue=self.audio_queue
        )
        dialog.exec()

    def on_audio_loaded(self, filename: str, count: int = 0) -> None:
        """Callback when audio is loaded"""
        self.status_bar.setText(f"Loaded: {filename}")

    def on_audio_complete(self, filename: str) -> None:
        """Callback when audio completes playback"""
        self.status_bar.setText(f"Playing: {filename}")

    def on_trigger_matched(self, filename: str) -> None:
        """Callback when trigger is matched"""
        self.media_bar.set_track(filename)
        self.status_bar.setText(f"Trigger matched: {filename}")
        self.media_bar.play()

    def play(self) -> None:
        """Play current audio"""
        if self.audio_queue.is_queueing():
            self.media_bar.update_playing_state(True)
            self.media_bar.play()
        else:
            self.media_bar.play()

    def pause(self) -> None:
        """Pause playback"""
        self.media_bar.pause()
        self.media_bar.update_playing_state(False)

    def stop(self) -> None:
        """Stop playback"""
        self.media_bar.stop()

    def toggle_pause(self) -> None:
        """Toggle pause state"""
        if self.audio_queue.is_queueing():
            self.media_bar.pause()
        else:
            self.media_bar.play()

    def get_audio_queue(self) -> "AudioQueue":
        """Get audio queue"""
        return self.audio_queue

    def get_trigger_classifier(self) -> "TriggerClassifier":
        """Get trigger classifier"""
        return self.trigger_classifier
