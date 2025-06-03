# AutomationDesigner/RunLoopHandler.py

import time
from PySide6.QtCore import QTimer


def runLoopHandler(self, start_node, stop_event, pause_event, EndNode, DelayNode):
    # 'self' is the AutomationDesigner instance
    start_id = start_node.id
    # print(f"[LoopWorker-{start_id}] Thread started.") # Optional

    try:
        while not stop_event.is_set():
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)
            if stop_event.is_set(): break

            self._highlight_node_in_path(start_id, start_node.id)
            
            start_node.process()
            current_node = start_node

            while True: 
                if isinstance(current_node, EndNode): break
                if stop_event.is_set(): break

                outputs = current_node.outputs()
                if not outputs: break

                out_port = outputs[list(outputs.keys())[0]]
                connected_ports = out_port.connected_ports()
                if not connected_ports: break

                next_node = connected_ports[0].node()
                if next_node is None: break
                if stop_event.is_set(): break

                self._clear_highlights_for_path(start_id)
                self._highlight_node_in_path(start_id, next_node.id)

                if isinstance(next_node, DelayNode):
                    next_node.process(stop_event=stop_event)
                else:
                    next_node.process()

                if stop_event.is_set(): return 
                current_node = next_node
            # End of inner traversal loop

            if stop_event.is_set(): break 

            if isinstance(current_node, EndNode):
                if current_node.get_property('repeat') == 'Single':
                    # REMOVE: self._loop_controller.node_started.emit(f"clear:{end_id}")
                    stop_event.set()

            self._loop_controller.loop_iteration_finished.emit(start_id)
            if stop_event.is_set(): break
    finally:
        if stop_event.is_set():
            print(f"[RUN_LOOP_DEBUG {start_id}] Loop ending, scheduling _clear_highlights_for_path via End block.")
            self._clear_highlights_for_path(start_id)