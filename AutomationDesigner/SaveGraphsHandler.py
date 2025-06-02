# AutomationDesigner/SaveGraphsHandler.py

import json

def saveGraphsHandler(self):
    try:
        graph_data = self._graph.serialize_session()

        with open(self.DEFAULT_GRAPH_FILE, 'w') as f:
            json.dump(graph_data, f, indent=4)

        print(f"[Main] Auto-saved graph to: {self.DEFAULT_GRAPH_FILE}")
    except Exception as e:
        print(f"[Main] Failed to auto-save graph on exit: {e}")