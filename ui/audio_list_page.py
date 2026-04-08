"""Audio library page showing all MP3 files"""
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QCheckBox, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog, QInputDialog, QDoubleSpinBox, QDialog, QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class AudioListPage(QWidget):
    """Page for managing audio library"""

    file_loaded = pyqtSignal(str)
    file_activated = pyqtSignal(str)
    current_file_changed = pyqtSignal(str)

    def __init__(self, trigger_classifier=None, audio_queue=None):
        super().__init__()
        self.trigger_classifier = trigger_classifier
        self.audio_queue = audio_queue
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the audio list page"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 5, 10, 5)  # Compact margins

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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Filename", "Trigger Phrase", "Volume", "Status", ""])
        # Set column 4 to stretch (Edit column with button)
        header = self.table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.currentRowChanged.connect(self._on_row_selected)
        self.table.itemDoubleClicked.connect(self._on_double_click)
        layout.addWidget(self.table)

        # Footer info
        info_layout = QHBoxLayout()

        self.file_count_label = QLabel("0 files loaded")
        info_layout.addWidget(self.file_count_label)

        info_layout.addStretch()

        layout.addLayout(info_layout)

    def _on_browse(self) -> None:
        """Handle folder browser"""
        folder, _ = QFileDialog.getExistingDirectory(
            self,
            "Select Audio Folder",
            "Music"
        )
        if folder:
            self._load_from_folder(folder)

    def _load_from_folder(self, folder: str) -> None:
        """Load all MP3 files from a folder"""
        from pathlib import Path
        folder_path = Path(folder)

        mp3_files = sorted(folder_path.glob("*.mp3"))

        if mp3_files:
            # Clear existing table
            self.table.setRowCount(0)

            # Add each file
            for mp3_file in mp3_files:
                filename = mp3_file.name
                # Generate trigger from filename
                trigger = filename.replace(".mp3", "").replace("_", " ").replace("-", " ")

                self.add_file(filename, trigger, 1.0, True)

                # Add to trigger classifier
                if self.trigger_classifier:
                    self.trigger_classifier.add_trigger(filename, trigger, volume=1.0)
        else:
            QMessageBox.information(self, "No Files Found",
                f"No MP3 files found in:\n{folder}")

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

        # Enabled column
        enabled_item = QTableWidgetItem()
        self.table.setItem(row, 3, enabled_item)

        # Edit button in last column
        btn = QPushButton("Edit")
        btn.setFixedWidth(60)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #5aabff;
            }
            QPushButton:pressed {
                background-color: #3a8eef;
            }
        """)
        btn.clicked.connect(lambda checked: self._on_edit_clicked(row))
        self.table.setCellWidget(row, 4, btn)

        # Update count
        self.file_count_label.setText(f"{self.table.rowCount()} files loaded")

    def _on_row_selected(self, row: int) -> None:
        """Handle row selection"""
        if row >= 0 and row < self.table.rowCount():
            item = self.table.item(row, 0)
            filename = item.text().split('\n')[0]
            self.current_file_changed.emit(filename)

    def _on_edit_clicked(self, row: int) -> None:
        """Handle edit button click"""
        item = self.table.item(row, 0)
        filename = item.text().split('\n')[0]
        self._open_edit_dialog(filename)

    def _on_double_click(self, item) -> None:
        """Handle double click to play file"""
        if item:
            filename = item.text().split('\n')[0]
            self.current_file_changed.emit(filename)

    def select_file(self, filename: str) -> None:
        """Explicitly select a file for playback"""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text().split('\n')[0] == filename:
                self.table.selectRow(row)
                self.current_file_changed.emit(filename)
                break

    def _open_edit_dialog(self, filename: str) -> None:
        """Open edit dialog for a file"""
        # Get current values

        # Get current values
        row = self.table.rowCount() - 1
        if row < 0:
            return
        trigger_item = self.table.item(row, 1)
        volume_item = self.table.item(row, 2)

        # Edit trigger phrase
        trigger = trigger_item.text()
        trigger_ok, trigger = QInputDialog.getText(
            self,
            "Edit Trigger Phrase",
            "Trigger phrase:",
            QLineEdit.Normal,
            trigger
        )

        if not trigger_ok:
            return

        trigger_item.setText(trigger)
        trigger_classifier = self.trigger_classifier
        if trigger_classifier:
            # Check if update_trigger method exists
            if hasattr(trigger_classifier, 'update_trigger'):
                trigger_classifier.update_trigger(filename, trigger)

        # Edit volume
        spin = QDoubleSpinBox()
        spin.setRange(0.1, 10.0)
        try:
            vol_val = float(volume_item.text().replace('x', ''))
            spin.setValue(vol_val)
        except ValueError:
            spin.setValue(1.0)
        spin.setSingleStep(0.5)
        spin.setFont(QFont("Arial", 10))

        # Create dialog
        spin_dialog = QDialog(self)
        spin_dialog.setWindowTitle("Edit Audio File")
        spin_layout = QVBoxLayout(spin_dialog)
        spin_layout.addWidget(spin)
        spin_dialog.exec()

        # Update volume if changed
        new_vol = spin.value()
        new_vol_text = f"{new_vol:.1f}x"
        volume_item.setText(new_vol_text)

        # Update trigger classifier
        if trigger_classifier:
            if hasattr(trigger_classifier, 'update_volume'):
                trigger_classifier.update_volume(filename, new_vol)

