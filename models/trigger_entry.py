"""Trigger entry data model"""
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class TriggerEntry:
    """Represents an audio file with its trigger settings"""
    file_path: Path
    filename: str
    trigger_phrase: Optional[str] = None
    description: Optional[str] = None
    volume: float = 1.0
    enabled: bool = True

    def __post_init__(self):
        # Auto-populate trigger from filename if not set
        if self.trigger_phrase is None:
            # Remove extension and underscores/hyphens from filename
            clean_name = self.filename.replace(
                ".mp3", ""
            ).replace("_", " ").replace("-", " ")
            self.trigger_phrase = clean_name.strip()

    @property
    def trigger_display(self) -> str:
        """Get display-friendly trigger phrase"""
        return self.trigger_phrase.replace("  ", " ") if self.trigger_phrase else "No trigger set"

    def to_dict(self) -> dict:
        return {
            "file_path": str(self.file_path),
            "filename": self.filename,
            "trigger_phrase": self.trigger_phrase,
            "description": self.description,
            "volume": self.volume,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TriggerEntry":
        return cls(
            file_path=Path(data["file_path"]),
            filename=data["filename"],
            trigger_phrase=data.get("trigger_phrase"),
            description=data.get("description"),
            volume=data.get("volume", 1.0),
            enabled=data.get("enabled", True)
        )
