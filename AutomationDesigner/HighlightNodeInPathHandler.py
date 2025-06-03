# AutomationDesigner/HighlightNodeInPathHandler.py

def highlightNodeInPathHandler(self, loop_start_id, node_id_to_highlight, NODE_HIGHLIGHT_COLOR):
    node = self._graph.get_node_by_id(node_id_to_highlight)
    if node:
        if loop_start_id not in self._active_paths_highlights:
            self._active_paths_highlights[loop_start_id] = set()

        node.set_color(*NODE_HIGHLIGHT_COLOR) 

        self._active_paths_highlights[loop_start_id].add(node_id_to_highlight)

        if hasattr(node, 'view') and hasattr(node.view, 'update'):
            node.view.update()
        self._view.update()
    else:
        print(f"  [DEBUG HIGHLIGHT] Node with ID '{node_id_to_highlight}' NOT FOUND.")