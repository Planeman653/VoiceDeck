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
        return 0 if self._on_complete_callback else (0 if self.queue else -1)

    @property
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.queue) == 0

    def is_queueing(self) -> bool:
        """Check if queue is actively queueing items"""
        return not self._is_paused and len(self.queue) > 0

    def _schedule_next_if_needed(self) -> None:
        """Schedule next item when current finishes"""
        # Directly check stream state without using is_playing()
        stream = self.player._stream
        is_stopped = (stream is None) or (stream.get_state() in ('stopped', 'finished')) if stream else True

        if is_stopped:
            if self.queue:
                item = self.queue.pop(0)
                self.player.play(item.file_path, volume=item.volume)
            else:
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
            # Resume only if there's a stream
            if self.player._stream:
                try:
                    self.player._stream.start()
                except Exception:
                    pass
