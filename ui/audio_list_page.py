"""Audio library page showing all MP3 files"""
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QCheckBox, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class AudioListPage(QWidget):
    """Page for managing audio library"""

    file_loaded = pyqtSignal(str)
    file_activated = pyqtSignal(str)

    def __init__(self, trigger_classifier, audio_queue):
        super().__init__()
        self.trigger_classifier = trigger_classifier
        self.audio_queue = audio_queue
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the audio list page"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("Audio Library")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # File browser button
        browser_btn = QPushButton("Browse Folders")
        browser_btn.setFixedHeight(30)
        browser_btn.clicked.connect(self._on_browse)
        header_layout.addWidget(browser_btn)

        layout.addLayout(header_layout)

        # Search/filter
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search files...")
        filter_layout.addWidget(self.filter_input, stretch=1)

        # Filter buttons
        filter_btn = QPushButton("Filter")
        filter_btn.setFixedHeight(30)
        filter_btn.clicked.connect(self._on_filter)
        filter_layout.addWidget(filter_btn)

        layout.addLayout(filter_layout)

        # Table for audio files
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Filename", "Trigger Phrase", "Volume", "Status"])
        # Set column 3 to stretch (last column with checkbox)
        header = self.table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # Footer info
        info_layout = QHBoxLayout()

        self.file_count_label = QLabel("0 files loaded")
        info_layout.addWidget(self.file_count_label)

        info_layout.addStretch()

        layout.addLayout(info_layout)

    def _on_browse(self) -> None:
        """Handle folder browser"""
        msg_box = QMessageBox()
        msg_box.information(self, "Folder Selection",
            "For now, drag and drop MP3 files into the app folder,\n"
            "or use Settings to set the audio folder path.")
        msg_box.exec()

    def _on_filter(self) -> None:
        """Handle filter"""
        filter_text = self.filter_input.text().lower()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if filter_text and filter_text not in item.text().lower():
                self.table.setRowHidden(i, True)
            elif not filter_text:
                self.table.setRowHidden(i, False)

    def add_file(self, filename: str, trigger_phrase: str, volume: float, enabled: bool) -> None:
        """Add file to library table"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Filename (with description)
        name_item = QTableWidgetItem(f"{filename}\n{trigger_phrase}")
        name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.table.setItem(row, 0, name_item)

        # Trigger phrase
        trigger_item = QTableWidgetItem(trigger_phrase)
        self.table.setItem(row, 1, trigger_item)

        # Volume
        vol_item = QTableWidgetItem(f"{volume:.1f}x")
        self.table.setItem(row, 2, vol_item)

        # Enabled checkbox
        cb_item = QTableWidgetItem()
        cb_widget = QCheckBox(enabled)
        cb_widget.setChecked(enabled)
        cb_widget.setStyleSheet("QCheckBox { padding: 4px; }")
        cb_widget.stateChanged.connect(
            lambda checked: self.on_enabled_changed(row, checked)
        )
        self.table.setCellWidget(row, 3, cb_widget)

        # Store trigger data
        self.table.setItemData(
            row,
            (filename, trigger_phrase, volume, enabled),
            Qt.ItemDataRole.UserRole
        )

        # Update count
        self.file_count_label.setText(f"{self.table.rowCount()} files loaded")

    def on_enabled_changed(self, row: int, enabled: bool) -> None:
        """Handle enabled checkbox change"""
        data = self.table.itemData(row, Qt.ItemDataRole.UserRole)
        if data:
            filename, trigger, volume, _ = data
            if not enabled:
                self.trigger_classifier.remove_trigger(filename)
            else:
                self.trigger_classifier.add_trigger(filename, trigger)

    def clear(self) -> None:
        """Clear library"""
        self.table.setRowCount(0)
        self.file_count_label.setText("0 files loaded")
