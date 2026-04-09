"""Audio queue for sequential playback"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class QueueItem:
    """Represents an item in the playback queue"""
    file_path: str
    volume: Optional[float] = None
    trigger_phrase: Optional[str] = None

    def __hash__(self):
        return hash(self.file_path)


class AudioQueue:
    """Manages audio playback queue"""

    def __init__(self, player: "AudioPlayer"):
        """Initialize audio queue

        Args:
            player: AudioPlayer instance
        """
        self.player = player
        self.queue: List[QueueItem] = []
        self._is_paused = False
        self._on_complete_callback = None

    def add(self, file_path: str, volume: float | None = None, trigger_phrase: str | None = None) -> None:
        """Add item to queue"""
        self.queue.append(QueueItem(file_path=file_path, volume=volume, trigger_phrase=trigger_phrase))
        self._schedule_next_if_needed()

    def remove(self, index: int) -> Optional[QueueItem]:
        """Remove item from queue by index"""
        if 0 <= index < len(self.queue):
            return self.queue.pop(index)
        return None

    def clear(self) -> None:
        """Clear all items from queue"""
        self.queue.clear()

    def current_index(self) -> int:
        """Get current queue index"""
        if self.player.is_playing():
            # For simplicity, just return position in list
            return 0
        return -1 if not self.queue else 0

    @property
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.queue) == 0

    def is_queueing(self) -> bool:
        """Check if queue is actively queueing items"""
        return self.player.is_playing() and not self._is_paused

    def _schedule_next_if_needed(self) -> None:
        """Schedule next item when current finishes"""
        if not self.player.is_playing() and self.queue:
            item = self.queue.pop(0)
            self.player.play(item.file_path, volume=item.volume)
        elif not self.queue:
            # No queue items, stop if playing
            if self.player.is_playing():
                self.player.stop()

    def _on_complete(self) -> None:
        """Callback when audio completes"""
        if self._on_complete_callback:
            self._on_complete_callback()
        self._schedule_next_if_needed()

    def set_complete_callback(self, callback) -> None:
        """Set callback for when audio completes"""
        self._on_complete_callback = callback

    def play_next(self) -> bool:
        """Play next item in queue"""
        if len(self.queue) > 0:
            item = self.queue.pop(0)
            return self.player.play(item.file_path, volume=item.volume)
        return False

    def stop(self) -> None:
        """Stop the queue"""
        self.player.stop()

    def stop_queue(self) -> None:
        """Stop the queue (alias for stop)"""
        self.stop()

    def pause(self) -> None:
        """Pause the queue"""
        self.player.pause()

    def toggle_pause(self) -> None:
        """Toggle pause state"""
        self._is_paused = not self._is_paused
        if self._is_paused:
            self.player.pause()
        else:
            self.player.resume()
