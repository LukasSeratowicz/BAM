# AutomationDesigner/CopyPasteEventHandler.py

from PySide6.QtCore import Qt

def copyPasteEventHandler(self, event):
    # Check for Ctrl+C (copy) or Ctrl+V (paste)
    if event.modifiers() == Qt.ControlModifier:
        if event.key() == Qt.Key.Key_C:
            self.copySelectedNodes()
            event.accept()
        elif event.key() == Qt.Key.Key_V:
            self.pasteSelectedNodes()
            event.accept()
        else:
            event.ignore()
    else:
        event.ignore()

def copySelectedNodesHandler(self):
    selected_nodes = self._graph.selected_nodes()
    if not selected_nodes:
        print("[Main] No nodes selected for copy.")
        return

    self._clipboard.clear()
    for node in selected_nodes:
        self._clipboard.append(node.copy())
    print(f"[Main] Copied {len(selected_nodes)} node(s).")

def pasteSelectedNodesHandler(self):
    if not self._clipboard:
        print("[Main] Clipboard is empty. Nothing to paste.")
        return

    for node in self._clipboard:
        new_node = node.copy()
        self._graph.add_node(new_node)
        print(f"[Main] Pasted node: {new_node.id}")

    #self.saveGraphs()
    print(f"[Main] Pasted {len(self._clipboard)} node(s) from clipboard.")
    #self._clipboard.clear()  # Clear clipboard after pasting