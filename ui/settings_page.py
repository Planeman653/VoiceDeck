"""Settings page for app configuration"""
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox,
    QComboBox, QLineEdit, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SettingsPage(QWidget):
    """Settings page"""

    def __init__(self, trigger_classifier, config):
        super().__init__()
        self.trigger_classifier = trigger_classifier
        self.config = config
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the settings page"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 5, 12, 5)  # Compact margins

        # AI Settings Section
        ai_section = QWidget()
        ai_layout = QVBoxLayout(ai_section)
        ai_layout.setSpacing(8)

        title_label = QLabel("AI Settings")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #4a9eff;")
        ai_layout.addWidget(title_label)

        # AI Model Selection
        model_layout = QHBoxLayout()
        model_label = QLabel("AI Model:")
        model_label.setFixedWidth(80)
        model_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.addItems(self.trigger_classifier.MODEL_SIZES)
        self.model_combo.setCurrentText("tiny")
        model_layout.addWidget(self.model_combo)

        ai_layout.addLayout(model_layout)

        # Sensitivity Slider
        sensitivity_layout = QHBoxLayout()
        sens_label = QLabel("AI Sensitivity:")
        sens_label.setFixedWidth(80)
        sensitivity_layout.addWidget(sens_label)

        self.sensitivity_slider = QSpinBox()
        self.sensitivity_slider.setRange(0, 100)
        self.sensitivity_slider.setValue(50)  # Default 50%
        self.sensitivity_slider.setSingleStep(5)
        self.sensitivity_slider.setFixedHeight(30)  # Compact height
        self.sensitivity_slider.setStyleSheet("""
            QSpinBox {
                padding: 2px 6px;
            }
        """)
        self.sensitivity_slider.valueChanged.connect(self._on_sensitivity_changed)
        sensitivity_layout.addWidget(self.sensitivity_slider, stretch=1)

        self.sensitivity_value = QLabel("50")
        self.sensitivity_value.setFixedWidth(50)
        sensitivity_layout.addWidget(self.sensitivity_value)

        sensitivity_hint = QLabel("(0 = Exact match, 100 = Loose)")
        sensitivity_hint.setFixedWidth(200)
        sensitivity_hint.setStyleSheet("color: #888; font-size: 10px;")
        sensitivity_layout.addWidget(sensitivity_hint)

        ai_layout.addLayout(sensitivity_layout)

        # Language Selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language:")
        lang_label.setFixedWidth(80)
        lang_layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh"])
        self.lang_combo.setCurrentText("en")
        lang_layout.addWidget(self.lang_combo)

        ai_layout.addLayout(lang_layout)

        # Enable listening toggle
        listen_layout = QHBoxLayout()
        listen_label = QLabel("Microphone Listening:")
        listen_label.setFixedWidth(80)
        listen_layout.addWidget(listen_label)

        self.listen_checkbox = QCheckBox("On")
        self.listen_checkbox.setChecked(True)
        listen_layout.addWidget(self.listen_checkbox)

        ai_layout.addLayout(listen_layout)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setFixedHeight(35)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        save_btn.clicked.connect(self._on_save)
        ai_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(ai_section)

        # About Section
        about_section = QWidget()
        about_layout = QVBoxLayout(about_section)
        about_layout.setSpacing(10)

        about_title = QLabel("About")
        about_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        about_title.setStyleSheet("color: #4a9eff;")
        about_layout.addWidget(about_title)

        about_text = QLabel(
            "VoiceDeck v1.0.0\n"
            "A voice-activated audio player for Windows.\n\n"
            "MIT License\n\n"
            "Features:\n"
            "- Local AI-powered trigger recognition\n"
            "- Configurable sensitivity\n"
            "- Sequential playback\n"
            "- Tray icon support"
        )
        about_text.setFont(QFont("Arial", 10))
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)

        layout.addWidget(about_section)

    def _on_sensitivity_changed(self, value: int) -> None:
        """Handle sensitivity slider change"""
        self.sensitivity_value.setText(str(value))

    def _on_save(self) -> None:
        """Handle save settings"""
        sensitivity = self.sensitivity_slider.value() / 100.0
        language = self.lang_combo.currentText()

        self.config["sensitivity"] = sensitivity
        self.config["ai_model"] = self.model_combo.currentText()
        self.config["language"] = language
        self.config["enable_listening"] = self.listen_checkbox.isChecked()

        QMessageBox.information(self, "Settings Saved", "Settings saved successfully!")

    def load_config(self) -> None:
        """Load current config values"""
        self.model_combo.setCurrentText(self.config.get("ai_model", "tiny"))
        self.sensitivity_slider.setValue(int(self.config.get("sensitivity", 0.5) * 100))
        self.sensitivity_value.setText(str(self.sensitivity_slider.value()))
        self.lang_combo.setCurrentText(self.config.get("language", "en"))
        self.listen_checkbox.setChecked(self.config.get("enable_listening", True))