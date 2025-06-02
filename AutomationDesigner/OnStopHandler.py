# AutomationDesigner/OnStopHandler.py


def onStopHandler(self, NODE_DEFAULT_COLOR, BackdropNode):
        for start_id, stop_event in self._loop_stop_flags.items():
            stop_event.set()
        # Clear pause flags as well
        for start_id, pause_event in self._loop_pause_flags.items():
            pause_event.clear()
        print("[Main] All loops stopped.")

        # Clear any existing highlight
        r, g, b = NODE_DEFAULT_COLOR
        for node in self._graph.all_nodes():
            node.set_color(r, g, b)
            if isinstance(node, BackdropNode):
                node.update()

        # Clear highlighted nodes and backdrops        
        self._highlighted_nodes.clear()
        self._highlighted_backdrops.clear()