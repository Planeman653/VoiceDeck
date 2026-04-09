"""Spotify-style media bar for playback controls"""
import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider, QApplication
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class MediaBar(QWidget):
    """Persistent media controls bar"""

    play_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    next_requested = pyqtSignal()
    prev_requested = pyqtSignal()
    volume_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    track_changed = pyqtSignal(str)
    play_current_requested = pyqtSignal()  # For manual play of current track

    def __init__(self):
        super().__init__()
        self.setObjectName("MediaBar")
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the media bar UI"""
        self.main_layout = QHBoxLayout(self)
        # Add top and bottom margin so media bar isn't cut off
        self.main_layout.setContentsMargins(0, 6, 0, 6)
        self.main_layout.setSpacing(8)

        # Play/Pause button
        self.play_btn = QPushButton("\u25B6 Play")
        self.play_btn.setFixedWidth(80)
        self.play_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.play_btn.clicked.connect(self._on_play_pause)

        # Stop button
        self.stop_btn = QPushButton("\u25C9 Stop")
        self.stop_btn.setFixedWidth(60)
        self.stop_btn.clicked.connect(self._on_stop)

        # Track info label
        self.track_label = QLabel("No track loaded")
        self.track_label.setFixedWidth(200)
        self.track_label.setFont(QFont("Arial", 10))
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setFixedHeight(6)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)  # Default 100%
        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        # Current volume label
        self.volume_label = QLabel("100%")
        self.volume_label.setFixedWidth(50)
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Assemble
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.stop_btn)

        self.main_layout.addLayout(controls_layout, 1)
        self.main_layout.addWidget(self.track_label)
        self.main_layout.addWidget(self.volume_slider)
        self.main_layout.addWidget(self.volume_label)

        # Add top margin so media bar isn't cut off
        self.main_layout.setContentsMargins(0, 4, 0, 0)
        self.main_layout.addStretch()

    def play(self) -> None:
        """Emitted when play is requested"""
        self.play_requested.emit()

    def play_current(self) -> None:
        """Play current track manually"""
        self.play_current_requested.emit()

    def pause(self) -> None:
        """Emitted when pause is requested"""
        self.pause_requested.emit()

    def stop(self) -> None:
        """Emitted when stop is requested"""
        self.stop_requested.emit()

    def next(self) -> None:
        """Emitted when next is requested"""
        self.next_requested.emit()

    def prev(self) -> None:
        """Emitted when previous is requested"""
        self.prev_requested.emit()

    def set_volume(self, volume: int) -> None:
        """Set volume percentage"""
        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_label.setText(f"{volume}%")
        self.volume_slider.blockSignals(False)
        self.volume_changed.emit(volume)

    def set_track(self, track_name: str) -> None:
        """Set currently playing track"""
        self.track_label.setText(track_name if track_name else "No track")
        self.track_changed.emit(track_name)

    def is_playing(self) -> bool:
        """Check if playing"""
        return False

    def _on_play_pause(self) -> None:
        """Play button click handler"""
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def _on_stop(self) -> None:
        """Stop button click handler"""
        self.stop_requested.emit()

    def _on_volume_changed(self, value: int) -> None:
        """Volume slider changed"""
        self.volume_changed.emit(value)

    def update_playing_state(self, is_playing: bool) -> None:
        """Update play button text"""
        if is_playing:
            self.play_btn.setText("\u23F8 Pause")
        else:
            self.play_btn.setText("\u25B6 Play")
