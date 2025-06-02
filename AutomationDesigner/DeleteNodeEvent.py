# AutomationDesigner/DeleteNodeEvent.py

from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt

def deleteNodeEventHandler(self, event: QKeyEvent):
    # Check for Delete or Backspace key
    if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
        selected_nodes = self._graph.selected_nodes()
        if selected_nodes:
            confirm = QMessageBox.question(self, "Delete Nodes",
                                        f"Are you sure you want to delete {len(selected_nodes)} selected node(s)?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for node in selected_nodes:
                    self._graph.remove_node(node)
                print(f"Deleted {len(selected_nodes)} node(s).")
                self.saveGraphs()
            event.accept()
            return