"""Upload dialog for adding audio files"""
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt


class UploadDialog(QDialog):
    """Dialog for uploading audio files"""

    def __init__(self, parent=None, trigger_classifier=None, audio_queue=None):
        super().__init__(parent)
        self.trigger_classifier = trigger_classifier
        self.audio_queue = audio_queue
        self.parent_window = parent
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
        """Handle files selected - actually add them to library"""
        if not files:
            return

        # Filter MP3 files
        filenames = [f for f in files if f.lower().endswith(".mp3")]
        if not filenames:
            QMessageBox.information(self, "No MP3 Files",
                "Please select MP3 files to upload.")
            return

        # Add each file to trigger classifier and audio list page
        import os
        for filepath in filenames:
            filename = os.path.basename(filepath)
            # Generate trigger from filename
            trigger = filename.replace(".mp3", "").replace("_", " ").replace("-", " ")

            # Add to trigger classifier with default volume
            if self.trigger_classifier:
                self.trigger_classifier.add_trigger(filename, trigger, volume=1.0)

            # Add to audio list page
            if self.parent_window and self.parent_window.tabs:
                audio_page = self.parent_window.tabs.widget(0)
                if audio_page:
                    audio_page.add_file(filename, trigger, 1.0, True)

        QMessageBox.information(self, "Files Uploaded",
            f"Successfully uploaded {len(filenames)} MP3 file(s)!\n"
            "They will now appear in the Library tab.")

        self.accept()
