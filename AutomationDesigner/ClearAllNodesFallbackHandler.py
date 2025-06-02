# AutomationDesigner/ClearAllNodesFallbackHandler.py

def clearAllNodesFallbackHandler(self):
    for node in list(self._graph.all_nodes()):
        self._graph.remove_node(node)
    print("[Main] All nodes cleared using fallback method.")