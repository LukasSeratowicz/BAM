# AutomationDesigner/OnLoadHandler.py

from PySide6.QtWidgets import QFileDialog, QMessageBox
import json
import os

def onLoadHandler(self, file_path=None):
    if file_path is None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Graph",
                                                self.DEFAULT_GRAPH_FILE,
                                                "Graph Files (*.json);;All Files (*)")
    if file_path and os.path.exists(file_path):
        self._on_stop() # Stop any running loops before loading a new graph
        try:
            # IMPORTANT: Before deserializing, clear existing nodes
            self._clear_all_nodes_fallback()

            # Read the JSON file content into a dictionary
            with open(file_path, 'r') as f:
                graph_data = json.load(f)

            # Deserialize the graph from the file
            self._graph.deserialize_session(graph_data)
            print(f"[Main] Graph loaded from: {file_path}")
            self.DEFAULT_GRAPH_FILE = file_path
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load graph: {e}\n"
                                "Please ensure node classes are registered.")
            print(f"[Main] Failed to load graph: {e}")
    elif file_path: # If file_path was provided but didn't exist (e.g., first launch)
        print(f"[Main] No graph file found at '{file_path}'. Starting with empty canvas.")
    else: # User cancelled file dialog
        print("[Main] Load operation cancelled.")