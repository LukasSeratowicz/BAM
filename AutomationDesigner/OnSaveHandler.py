# AutomationDesigner/OnSaveHandler.py

from PySide6.QtWidgets import QFileDialog, QMessageBox
import json

def onSaveHandler(self):
    file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph",
                                                 self.DEFAULT_GRAPH_FILE,
                                                 "Graph Files (*.json);;All Files (*)")
    if file_path:
        try:
            graph_data = self._graph.serialize_session()

            # 2. Manually write the dictionary to the specified JSON file
            with open(file_path, 'w') as f:
                json.dump(graph_data, f, indent=4) # Using indent for readability in the JSON file

            print(f"[Main] Graph saved to: {file_path}")
            self.DEFAULT_GRAPH_FILE = file_path
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save graph: {e}")
            print(f"[Main] Failed to save graph: {e}")