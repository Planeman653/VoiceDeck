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
        self.model_combo.setFixedHeight(30)
        self.model_combo.setStyleSheet("""
            QComboBox {
                padding: 2px 6px;
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
            }
        """)
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
        self.sensitivity_slider.setFixedHeight(30)
        self.sensitivity_slider.setStyleSheet("""
            QSpinBox {
                padding: 6px 10px;
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #3b3b3b;
                selection-background-color: #4a9eff;
                font-size: 12px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #4a4a6a;
                border: none;
            }
        """)
        self.sensitivity_slider.valueChanged.connect(self._on_sensitivity_changed)
        sensitivity_layout.addWidget(self.sensitivity_slider, stretch=1)

        self.sensitivity_value = QLabel("50")
        self.sensitivity_value.setFixedWidth(50)
        self.sensitivity_value.setStyleSheet("""
            QLabel {
                padding: 4px 8px;
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #3b3b3b;
                font-weight: bold;
                font-size: 12px;
            }
        """)
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
        self.lang_combo.setFixedHeight(30)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                padding: 2px 6px;
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
            }
        """)
        lang_layout.addWidget(self.lang_combo)

        ai_layout.addLayout(lang_layout)

        # Enable listening toggle
        listen_layout = QHBoxLayout()
        listen_label = QLabel("Microphone Listening:")
        listen_label.setFixedWidth(80)
        listen_layout.addWidget(listen_label)

        self.listen_checkbox = QCheckBox("On")
        self.listen_checkbox.setChecked(True)
        self.listen_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                background-color: #2b2b2b;
                padding: 4px 8px;
            }
        """)
        listen_layout.addWidget(self.listen_checkbox)

        ai_layout.addLayout(listen_layout)

        # Device Settings Section
        device_section = QWidget()
        device_layout = QVBoxLayout(device_section)
        device_layout.setSpacing(8)

        device_title = QLabel("Audio Devices")
        device_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        device_title.setStyleSheet("color: #4a9eff;")
        device_layout.addWidget(device_title)

        # Output device selection
        output_layout = QHBoxLayout()
        output_label = QLabel("Output Device:")
        output_label.setFixedWidth(90)
        output_label.setStyleSheet("color: #ccc;")
        output_layout.addWidget(output_label)

        self.output_combo = QComboBox()
        self.output_combo.setFixedHeight(30)
        self.output_combo.setStyleSheet("""
            QComboBox {
                padding: 2px 6px;
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
            }
        """)
        self.output_combo.currentIndexChanged.connect(self._on_output_device_changed)
        output_layout.addWidget(self.output_combo)

        output_hint = QLabel("(Speakers/Headphones)")
        output_hint.setFixedWidth(150)
        output_hint.setStyleSheet("color: #888; font-size: 10px;")
        output_layout.addWidget(output_hint)

        device_layout.addLayout(output_layout)

        # Input device selection
        input_layout = QHBoxLayout()
        input_label = QLabel("Input Device:")
        input_label.setFixedWidth(90)
        input_label.setStyleSheet("color: #ccc;")
        input_layout.addWidget(input_label)

        self.input_combo = QComboBox()
        self.input_combo.setFixedHeight(30)
        self.input_combo.setStyleSheet("""
            QComboBox {
                padding: 2px 6px;
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
            }
        """)
        self.input_combo.currentIndexChanged.connect(self._on_input_device_changed)
        input_layout.addWidget(self.input_combo)

        input_hint = QLabel("(Microphone)")
        input_hint.setFixedWidth(100)
        input_hint.setStyleSheet("color: #888; font-size: 10px;")
        input_layout.addWidget(input_hint)

        device_layout.addLayout(input_layout)

        # Load available devices
        self._load_devices()

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
        device_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

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
            "- Device selection (Input/Output)\n"
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

    def load_config(self) -> None:
        """Load current config values"""
        self.model_combo.setCurrentText(self.config.get("ai_model", "tiny"))
        self.sensitivity_slider.setValue(int(self.config.get("sensitivity", 0.5) * 100))
        self.sensitivity_value.setText(str(self.sensitivity_slider.value()))
        self.lang_combo.setCurrentText(self.config.get("language", "en"))
        self.listen_checkbox.setChecked(self.config.get("enable_listening", True))

    def _load_devices(self) -> None:
        """Load available audio devices from config"""
        try:
            from audio_manager import AudioPlayer
            player = AudioPlayer()
            devices = player.get_devices()
            if devices:
                # Clear existing items
                self.output_combo.clear()
                self.input_combo.clear()
                # Load output devices (only output-capable)
                for dev in devices:
                    out_ch = dev.get('max_output_channels') or dev.get('MaxOutputChannels')
                    if out_ch is not None and out_ch > 0:
                        name = dev.get('name', dev.get('Name', ''))
                        if name.strip():
                            self.output_combo.addItem(name, dev.get('index', dev.get('Index', 0)))
                # Load input devices (only input-capable)
                for dev in devices:
                    in_ch = dev.get('max_input_channels') or dev.get('MaxInputChannels')
                    if in_ch is not None and in_ch > 0:
                        name = dev.get('name', dev.get('Name', ''))
                        if name.strip():
                            self.input_combo.addItem(name, dev.get('index', dev.get('Index', 0)))
                # Set current index from config
                self._set_device_from_config()
        except Exception as e:
            print(f"Error loading devices: {e}")

    def _set_device_from_config(self) -> None:
        """Set device selection from config values"""
        try:
            from audio_manager import AudioPlayer
            player = AudioPlayer()
            # Try to set devices from current AudioPlayer instance
            if hasattr(player, 'output_device') and player.output_device is not None:
                self.output_combo.setCurrentIndex(player.output_device)
            if hasattr(player, 'input_device') and player.input_device is not None:
                self.input_combo.setCurrentIndex(player.input_device)
        except Exception:
            pass

    def _on_output_device_changed(self, index: int) -> None:
        """Handle output device change"""
        if index >= 0:
            device_index = self.output_combo.itemData(index)
            try:
                from audio_manager import AudioPlayer
                player = AudioPlayer()
                player.set_device("output", device_index)
            except Exception:
                pass

    def _on_input_device_changed(self, index: int) -> None:
        """Handle input device change"""
        if index >= 0:
            device_index = self.input_combo.itemData(index)
            try:
                from audio_manager import AudioPlayer
                player = AudioPlayer()
                player.set_device("input", device_index)
            except Exception:
                pass

    def _on_save(self) -> None:
        """Handle save settings"""
        sensitivity = self.sensitivity_slider.value() / 100.0
        language = self.lang_combo.currentText()
        enable_listening = self.listen_checkbox.isChecked()

        self.config["sensitivity"] = sensitivity
        self.config["ai_model"] = self.model_combo.currentText()
        self.config["language"] = language
        self.config["enable_listening"] = enable_listening

        # Save device settings
        self.config["output_device_index"] = self.output_combo.currentIndex() if self.output_combo.currentIndex() >= 0 else None
        self.config["input_device_index"] = self.input_combo.currentIndex() if self.input_combo.currentIndex() >= 0 else None

        QMessageBox.information(self, "Settings Saved", "Settings saved successfully!")