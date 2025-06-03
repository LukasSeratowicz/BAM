# AutomationDesigner/ClearHighlightsForPathHandler.py

def clearHighlightsForPathHandler(self, loop_start_id: str, NODE_DEFAULT_COLOR):
    if loop_start_id in self._active_paths_highlights:
        path_node_ids_to_clear = self._active_paths_highlights.pop(loop_start_id, set())
        for node_id in path_node_ids_to_clear:
            node = self._graph.get_node_by_id(node_id)
            if node:
                is_in_another_active_path = False
                for other_sid, other_path_nodes in self._active_paths_highlights.items():
                    if node_id in other_path_nodes:
                        is_in_another_active_path = True
                        break
                if not is_in_another_active_path:
                    node.set_color(*NODE_DEFAULT_COLOR)
                    if hasattr(node, 'view') and hasattr(node.view, 'update'):
                        node.view.update()
                self._view.update()
        if not path_node_ids_to_clear:
            print(f"  [DEBUG DE-HIGHLIGHT] Path '{loop_start_id}' had no nodes in _active_paths_highlights to clear.")
    else:
        print(f"  [DEBUG DE-HIGHLIGHT] No active path highlight data found for loop_start_id='{loop_start_id}'.")