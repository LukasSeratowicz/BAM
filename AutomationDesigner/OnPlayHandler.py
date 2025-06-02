# AutomationDesigner/OnPlayHandler.py

from PySide6.QtWidgets import QMessageBox
import threading

def onPlayHandler(self, NODE_DEFAULT_COLOR, StartNode):
    r, g, b = NODE_DEFAULT_COLOR
    for node in self._graph.all_nodes():
        node.set_color(r, g, b)
    self._last_highlighted_node = None

    self._highlighted_nodes.clear()
    self._highlighted_backdrops.clear()

    # Find all StartNode instances using all_nodes()
    all_nodes = self._graph.all_nodes()
    start_nodes = [n for n in all_nodes if isinstance(n, StartNode)]

    if not start_nodes:
        QMessageBox.warning(self, "No Start Node", "Please add at least one Start node before playing.")
        return

    for start_node in start_nodes:
        start_id = start_node.id
        
        if start_id not in self._loop_threads or not self._loop_threads[start_id].is_alive():
            stop_event = threading.Event()
            pause_event = threading.Event()
            self._loop_stop_flags[start_id] = stop_event
            self._loop_pause_flags[start_id] = pause_event

            thread = threading.Thread(
                target=self._run_loop,
                args=(start_node, stop_event, pause_event),
                daemon=True
            )
            self._loop_threads[start_id] = thread
            thread.start()
            print(f"[Main] Launched loop thread for Start Node {start_id}")
        elif start_id in self._loop_pause_flags:
            self._loop_pause_flags[start_id].clear()
            print(f"[Main] Unpaused loop thread for Start Node {start_id}")
        else:
            print(f"[Main] Start Node {start_id} is already running and not in a pausable state (or not previously paused).")