# AutomationDesigner/KeyPressEvent.py

def createNodeHandler(self, node_label, node_map):
        NodeClass = node_map.get(node_label)
        if NodeClass is None:
            return

        new_node = NodeClass()
        self._graph.add_node(new_node)
        new_node.set_pos(self._last_scene_pos.x(), self._last_scene_pos.y())