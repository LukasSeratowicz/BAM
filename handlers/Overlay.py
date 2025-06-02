# handlers/Overlay.py

import asyncio
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
)
show_coords = False
mouse_x, mouse_y = 0, 0


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label = QLabel("", self)
        self.label.setStyleSheet("color: white; background-color: rgba(0,0,0,0); font-size: 16px;")
        self.label.move(0, 0)
        self.resize(200, 30)
        self.hide()

    def update_text(self, x, y):
        """
        Update the overlay text with the current mouse coordinates.
        """
        self.label.setText(f"X: {x}  Y: {y}")
        self.label.adjustSize()
        self.resize(self.label.size())

    def show_at_top_right(self):
        """
        Move the overlay to the top-right corner of the primary screen.
        """
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() - self.width(), 0)
        self.show()

async def overlay_update_loop():
    """
    Main loop to update the overlay with mouse coordinates.
    This runs asynchronously and updates the overlay every 50ms.
    """
    overlay = Overlay()

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(50)

    while True:
        if show_coords:
            overlay.update_text(mouse_x, mouse_y)
            if not overlay.isVisible():
                overlay.show_at_top_right()
        else:
            if overlay.isVisible():
                overlay.hide()
        await asyncio.sleep(0.05)