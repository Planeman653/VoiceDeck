"""Application configuration and settings"""
import json
from pathlib import Path
from typing import Any


class AppConfig:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        "audio_folder": "resources/audio",
        "default_volume": 1.0,
        "ai_model": "tiny",
        "sensitivity": 50,
        "enable_listening": True,
        "language": "en",
        "theme": "dark"
    }

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config: dict = self.DEFAULT_CONFIG.copy()
        self._load_config()

    def _load_config(self) -> None:
        """Load config from file if it exists"""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    for key, value in user_config.items():
                        if key in self.config:
                            self.config[key] = value
            except (json.JSONDecodeError, IOError):
                pass

    def save(self) -> None:
        """Save config to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set config value"""
        if key in self.config:
            self.config[key] = value
            self.save()
