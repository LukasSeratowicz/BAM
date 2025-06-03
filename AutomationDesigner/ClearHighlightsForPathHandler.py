# AutomationDesigner/ClearHighlightsForPathHandler.py

# In main.py, class AutomationDesigner
def _update_all_backdrop_highlights(self, BackdropNode, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR):
    all_currently_highlighted_execution_node_ids = set(self._active_paths_highlights.values())
    
    for bp_node in self._graph.all_nodes():
        if isinstance(bp_node, BackdropNode):
            should_this_backdrop_be_highlighted = False
            for exec_node_id in all_currently_highlighted_execution_node_ids:
                exec_node = self._graph.get_node_by_id(exec_node_id)
                if exec_node and exec_node in bp_node.nodes():
                    should_this_backdrop_be_highlighted = True
                    break 
            
            current_bp_color_prop = bp_node.properties().get('color', NODE_DEFAULT_COLOR)
            
            if should_this_backdrop_be_highlighted:
                target_bp_color = NODE_HIGHLIGHT_COLOR
            else:
                target_bp_color = NODE_DEFAULT_COLOR
            
            if tuple(current_bp_color_prop[:3]) != tuple(target_bp_color[:3]):
                bp_node.set_color(*target_bp_color)
                bp_node.update()

def clearHighlightsForPathHandler(self, loop_start_id: str, BackdropNode, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR):
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
        _update_all_backdrop_highlights(self, BackdropNode, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR)