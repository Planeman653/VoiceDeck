"""Upload dialog for adding audio files"""
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt


class UploadDialog(QDialog):
    """Dialog for uploading audio files"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the upload dialog"""
        self.setWindowTitle("Upload MP3 Files")
        self.setMinimumSize(500, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Instruction
        instruction = QLabel(
            "Select MP3 files from your computer to add to the library.\n"
            "The trigger phrase will be auto-detected from the filename."
        )
        instruction.setWordWrap(True)
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction)

        # Browse button
        browse_btn = QPushButton("Browse for MP3 Files...")
        browse_btn.setFixedHeight(40)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00d4aa;
            }
        """)
        browse_btn.clicked.connect(self._on_browse)
        layout.addWidget(browse_btn)

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _on_browse(self) -> None:
        """Handle browse button click"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select MP3 Files",
            "",
            "MP3 Files (*.mp3);;All Files (*.*)"
        )

        if files:
            self.on_files_selected(files)

    def on_files_selected(self, files: list) -> None:
        """Handle files selected"""
        if not files:
            return

        # For now, just show confirmation
        filenames = [f for f in files if f.lower().endswith(".mp3")]
        if filenames:
            QMessageBox.information(self, "Files Selected",
                f"You selected {len(filenames)} MP3 file(s).\n"
                "For now, drag and drop them into the app folder\n"
                "or set the audio folder path in Settings.")

        self.accept()
