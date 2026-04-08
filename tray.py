"""Tray icon for app (simple minimize/close)"""
import sys
from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt


class SimpleTray:
    """Simple tray icon - just minimize to tray"""

    def __init__(self, app, window):
        """Initialize tray

        Args:
            app: QApplication instance
            window: MainWindow instance to hide/show
        """
        self.app = app
        self.window = window

        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self._create_icon())
        self.tray_icon.setContextMenu(self._create_context_menu())
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def _create_icon(self) -> QIcon:
        """Create tray icon from app name"""
        return QIcon.fromTheme("audio-player") or self._create_default_icon()

    def _create_default_icon(self) -> QIcon:
        """Create default icon using QPixmap"""
        from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor
        from PyQt6.QtWidgets import QApplication

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw microphone icon (simplified)
        painter.setPen(QColor("#4a9eff"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "VD")

        painter.end()

        return QIcon(pixmap)

    def _create_context_menu(self):
        """Create system tray context menu"""
        from PyQt6.QtWidgets import QMenu
        menu = QMenu()

        show_action = QAction("Show Window", self.window)
        show_action.triggered.connect(self._show_window)
        menu.addAction(show_action)

        quit_action = QAction("Quit", self.window)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)

        return menu

    def _on_tray_activated(self, reason: Qt.TrayIconActivationReason) -> None:
        """Handle tray icon activation"""
        if reason == Qt.TrayIconActivationReason.DoubleClick:
            self._show_window()

    def _show_window(self) -> None:
        """Show the main window"""
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def hide(self) -> None:
        """Hide the main window (minimize to tray)"""
        self.window.hide()