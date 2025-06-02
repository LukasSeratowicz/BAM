# handlers/LoopController.py

from PySide6.QtCore import (
    Signal, 
    QObject,
)

class LoopController(QObject):
    loop_iteration_finished = Signal(str)
    node_started = Signal(str)