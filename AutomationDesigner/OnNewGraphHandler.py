# AutomationDesigner/OnNewGraphHandler.py

from PySide6.QtWidgets import QMessageBox

def onNewGraphHandler(self):
    reply = QMessageBox.question(self, "New Graph",
                                        "Are you sure you want to create a new graph? Any unsaved changes will be lost.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        self._on_stop() # Stop any running loops first
        self._clear_all_nodes_fallback()
        print("[Main] New graph created.")
