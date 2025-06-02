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
    selected = self._graph.selected_nodes()
    if not selected:
        print("[Main] No nodes selected for copy.")
        return

    # Erase any previous clipboard contents:
    self._clipboard = []

    # For each selected node, store (original, one‐time copy) pair:
    for node in selected:
        copied_node = node.copy()
        self._clipboard.append((node, copied_node))

    print(f"[Main] Copied {len(self._clipboard)} node(s).")

def pasteSelectedNodesHandler(self):
    if not getattr(self, "_clipboard", None):
        print("[Main] Clipboard is empty. Nothing to paste.")
        return

    # 1) Insert each copied_node into the graph.
    for orig, copied_node in self._clipboard:
        self._graph.add_node(copied_node)
        print(f"[Main] Pasted node: {copied_node.id}")

    # 2) Build a mapping: original_id → new_copy_instance
    orig_to_new = { orig.id: new for (orig, new) in self._clipboard }

    # 3) For each (orig, new_node), walk orig.output_ports() and reconnect:
    for orig, new_node in self._clipboard:
        # out_port is a Port object on the original node
        for out_port in orig.output_ports():
            # connected_ports() returns a list of Port objects to which out_port is connected
            for dest_port in out_port.connected_ports():
                dest_node = dest_port.node()
                # Only rewire if dest_node was also in the original selection
                if dest_node.id in orig_to_new:
                    new_dest = orig_to_new[dest_node.id]

                    # Get the matching Port objects on the new copies:
                    new_src_port = new_node.get_output(out_port.name())
                    new_dst_port = new_dest.get_input(dest_port.name())

                    # Now recreate the connection
                    new_src_port.connect_to(new_dst_port)

    print(f"[Main] Recreated connections among pasted nodes.")

    # 4) Reselect newly pasted nodes as a group
    new_nodes = [new for (_, new) in self._clipboard]
    self._graph.clear_selection()
    for n in new_nodes:
        n.set_selected(True)

    print(f"[Main] Finished pasting {len(self._clipboard)} node(s).")