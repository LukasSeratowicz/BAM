# AutomationDesigner/HighlightNodeInPathHandler.py

def updateAllBackdropsHighlightsHandler(self, BackdropNode, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR):
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

def highlightNodeInPathHandler(self, loop_start_id, node_id_to_highlight_now, NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR):
    prev_highlighted_node_id_for_this_loop = self._active_paths_highlights.get(loop_start_id)
    node_to_highlight_obj = self._graph.get_node_by_id(node_id_to_highlight_now)

    # 1. Unhighlight the previous node of THIS path, if it exists and is different
    if prev_highlighted_node_id_for_this_loop and prev_highlighted_node_id_for_this_loop != node_id_to_highlight_now:
        prev_node_obj = self._graph.get_node_by_id(prev_highlighted_node_id_for_this_loop)
        if prev_node_obj:
            is_prev_node_still_highlighted_by_another_path = False
            # Check if this prev_node_id is the currently highlighted node in ANY OTHER path
            for other_loop_s_id, active_node_id_in_other_loop in self._active_paths_highlights.items():
                if other_loop_s_id != loop_start_id: # Must be a different path
                    if active_node_id_in_other_loop == prev_highlighted_node_id_for_this_loop:
                        is_prev_node_still_highlighted_by_another_path = True
                        break
            if not is_prev_node_still_highlighted_by_another_path:
                prev_node_obj.set_color(*NODE_DEFAULT_COLOR)

    # 2. Highlight the new current node for THIS path
    if node_to_highlight_obj:
        node_to_highlight_obj.set_color(*NODE_HIGHLIGHT_COLOR)
        self._active_paths_highlights[loop_start_id] = node_id_to_highlight_now

    # 3. Update all backdrop highlights based on the current state of _active_paths_highlights
    if hasattr(self, '_update_all_backdrop_highlights'):
        self._update_all_backdrop_highlights(NODE_HIGHLIGHT_COLOR, NODE_DEFAULT_COLOR)
