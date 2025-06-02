# AutomationDesigner/OnNodeStartedHandler.py



def onNodeStartedHandler(self, msg, NODE_DEFAULT_COLOR, NODE_HIGHLIGHT_COLOR, BackdropNode):
    # ─── CASE A: a clear‐request for a particular node/backdrop ───
    if msg.startswith("clear:"):
        _, nid = msg.split(":", 1)
        # 1) Clear that node, if currently highlighted
        if nid in self._highlighted_nodes:
            node = self._graph.get_node_by_id(nid)
            if node:
                r, g, b = NODE_DEFAULT_COLOR
                node.set_color(r, g, b)
                # no need to call update() for normal nodes
            self._highlighted_nodes.remove(nid)

        # 2) Also clear its enclosing backdrop, if any
        #    We must find which backdrop contains that node
        node = self._graph.get_node_by_id(nid)
        if node:
            for bp in self._graph.all_nodes():
                if isinstance(bp, BackdropNode):
                    # if node is inside bp.nodes(), clear bp
                    if node in bp.nodes():
                        bid = bp.id
                        if bid in self._highlighted_backdrops:
                            r, g, b = NODE_DEFAULT_COLOR
                            bp.set_color(r, g, b)
                            bp.update()  # force redraw
                            self._highlighted_backdrops.remove(bid)
                        break
        return

    # ─── CASE B: a normal node_id to highlight ───
    node_id = msg
    node = self._graph.get_node_by_id(node_id)
    if not node:
        return

    # 1) Determine which backdrop (if any) contains this node:
    current_bp = None
    for bp in self._graph.all_nodes():
        if isinstance(bp, BackdropNode) and node in bp.nodes():
            current_bp = bp
            break

    # 2) If there is a backdrop, clear only its old highlighted member(s);
    #    otherwise (no backdrop) clear all previously highlighted nodes.
    if current_bp:
        to_remove = []
        for old_nid in self._highlighted_nodes:
            old_node = self._graph.get_node_by_id(old_nid)
            if old_node and old_node in current_bp.nodes():
                # un‐highlight old_node
                r0, g0, b0 = NODE_DEFAULT_COLOR
                old_node.set_color(r0, g0, b0)
                to_remove.append(old_nid)
        for old_nid in to_remove:
            self._highlighted_nodes.remove(old_nid)
    else:
        # no backdrop: clear every previously highlighted node
        for old_nid in list(self._highlighted_nodes):
            old_node = self._graph.get_node_by_id(old_nid)
            if old_node:
                r0, g0, b0 = NODE_DEFAULT_COLOR
                old_node.set_color(r0, g0, b0)
            self._highlighted_nodes.remove(old_nid)

    # 3) Now highlight the new node (if not already):
    if node_id not in self._highlighted_nodes:
        r, g, b = NODE_HIGHLIGHT_COLOR
        node.set_color(r, g, b)
        self._highlighted_nodes.add(node_id)

    # 4) Highlight the backdrop itself (once) if not already:
    if current_bp:
        bid = current_bp.id
        if bid not in self._highlighted_backdrops:
            r, g, b = NODE_HIGHLIGHT_COLOR
            current_bp.set_color(r, g, b)
            current_bp.update()
            self._highlighted_backdrops.add(bid)