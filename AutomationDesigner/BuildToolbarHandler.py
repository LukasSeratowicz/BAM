# AutomationDesigner/BuildToolbarHandler.py

from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

def buildToolbarHandler(self):
        toolbar = QToolBar("Controls", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Play button
        self._play_action = QAction("Play", self)
        self._play_action.triggered.connect(self._on_play)
        toolbar.addAction(self._play_action)

        # Pause button
        self._pause_action = QAction("Pause", self)
        self._pause_action.triggered.connect(self._on_pause)
        toolbar.addAction(self._pause_action)

        # Stop button
        self._stop_action = QAction("Stop", self)
        self._stop_action.triggered.connect(self._on_stop)
        toolbar.addAction(self._stop_action)