# AutomationDesigner/ClearHighlightsForPathHandler.py

def clearHighlightsForPathHandler(self, loop_start_id: str, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR):
    last_highlighted_node_id_for_this_loop = self._active_paths_highlights.pop(loop_start_id, None)

    if last_highlighted_node_id_for_this_loop:
        node_to_clear_obj = self._graph.get_node_by_id(last_highlighted_node_id_for_this_loop)
        if node_to_clear_obj:
            is_node_still_highlighted_by_another_path = False
            # Check if this node_id is still the active highlight in any *other remaining* paths
            for active_node_id_in_other_loop in self._active_paths_highlights.values():
                if active_node_id_in_other_loop == last_highlighted_node_id_for_this_loop:
                    is_node_still_highlighted_by_another_path = True
                    break
            if not is_node_still_highlighted_by_another_path:
                node_to_clear_obj.set_color(*NODE_DEFAULT_COLOR)

    # Update all backdrop highlights after this path's node is cleared
    if hasattr(self, '_update_all_backdrop_highlights'):
        self._update_all_backdrop_highlights(NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR)