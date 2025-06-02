# AutomationDesigner/CopyPasteEventHandler.py

from PySide6.QtCore import Qt, QTimer
import traceback

def copyPasteEventHandler(self, event):
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
        print("[Main_Copy] No nodes selected for copy.")
        return

    self._clipboard = []
    for node in selected:
        # Corrected line: node.id is an attribute, not a method
        if hasattr(node, 'copy') and callable(node.copy):
            entry = node.copy()
            self._clipboard.append(entry)
        else:
            print(f"[Main_Copy] ERROR: Node {node.id} has no 'copy' method!") # Corrected here too

def pasteSelectedNodesHandler(self):
    if not getattr(self, "_clipboard", None) or not self._clipboard:
        print("[Main_Paste] Clipboard is empty. Nothing to paste.")
        return

    orig_to_new = {}
    newly_created_nodes_for_props = []

    for i, (orig_id, NodeClass, props_from_copy, (x_orig, y_orig)) in enumerate(self._clipboard):
        new_node = NodeClass()
        self._graph.add_node(new_node)
        new_pos_x, new_pos_y = x_orig + 20, y_orig + 20
        new_node.set_pos(new_pos_x, new_pos_y)
        orig_to_new[orig_id] = new_node
        newly_created_nodes_for_props.append({'node': new_node, 'props': props_from_copy, 'orig_id': orig_id})

    if not newly_created_nodes_for_props:
        print("[Main_Paste] No nodes were actually created from clipboard.")
        return
        
    def apply_all_properties():
        for item_idx, item in enumerate(newly_created_nodes_for_props):
            node_to_set = item['node']
            copied_props = item['props']

            for name, val in copied_props.items():
                try:
                    if name in ['id', 'pos', 'selected', 'type_']:
                        continue

                    if name == 'color':
                        if isinstance(val, (list, tuple)) and len(val) in (3, 4) and all(isinstance(x, int) for x in val):
                            color_list_to_set = list(val)
                            node_to_set.set_property(name, color_list_to_set, push_undo=False)
                    elif hasattr(node_to_set, f'set_{name}'):
                        setter_method = getattr(node_to_set, f'set_{name}')
                        setter_method(val)
                    else:
                        node_to_set.set_property(name, val, push_undo=False)
                except Exception:
                    traceback.print_exc() 

    QTimer.singleShot(0, apply_all_properties)

    # Connection Rebuilding 
    for orig_id_conn, _, _, _ in self._clipboard:
        try:
            original_node_in_graph = next(n for n in self._graph.all_nodes() if n.id == orig_id_conn)
            newly_pasted_node_equivalent = orig_to_new[orig_id_conn]

            for out_port in original_node_in_graph.output_ports():
                for original_dest_port in out_port.connected_ports():
                    original_dest_node_id = original_dest_port.node().id
                    
                    if original_dest_node_id in orig_to_new: 
                        new_source_node_for_conn = newly_pasted_node_equivalent
                        new_dest_node_for_conn = orig_to_new[original_dest_node_id]
                        
                        new_src_port = new_source_node_for_conn.get_output(out_port.name())
                        new_dst_port = new_dest_node_for_conn.get_input(original_dest_port.name())

                        if new_src_port and new_dst_port:
                            new_src_port.connect_to(new_dst_port)
        except Exception: 
            pass 

    # Reselection
    new_nodes_instances = list(orig_to_new.values())
    if new_nodes_instances:
        self._graph.clear_selection()
        for n_instance in new_nodes_instances:
            n_instance.set_selected(True)