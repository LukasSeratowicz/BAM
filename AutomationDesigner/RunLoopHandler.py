# AutomationDesigner/RunLoopHandler.py

import shared.globals as g

import time
from PySide6.QtCore import QTimer


def runLoopHandler(self, start_node, stop_event, pause_event, EndNode, DelayNode):
    start_id = start_node.id
    print(f"[LoopWorker-{start_id}] Thread started.")

    while not stop_event.is_set():
        # 1) Handle Pause: if pause_event is set, wait until it’s cleared
        while pause_event.is_set() and not stop_event.is_set():
            time.sleep(0.1)

        if stop_event.is_set():
            break

        # 1.2) Highlight the Start node that just started
        self._loop_controller.node_started.emit(start_node.id)
        
        # 2) “Fire” the Start node
        start_node.process()

        # 3) Traverse the graph from StartNode → … → EndNode
        current_node = start_node

        while True:
            # If current_node is already an EndNode, break out
            if isinstance(current_node, EndNode):
                break

            # Get all output ports (as a dict: { port_name: port_obj, ... })
            outputs = current_node.outputs()
            port_names = list(outputs.keys())
            print(f"[Debug] Node {current_node.id} output ports: {port_names}")

            if not port_names:
                # No outputs → stop traversal
                break

            # Take the first output port
            out_port = current_node.outputs()[list(current_node.outputs().keys())[0]]
            connected_ports = out_port.connected_ports()
            print(f"[Debug] Traversal at node {current_node.id}, connected_ports: {connected_ports}")

            if not connected_ports:
                # No outgoing connections → stop
                break

            # Take the first connection: (next_node_id, next_port_name)
            next_node = connected_ports[0].node()
            next_node_id = next_node.id
            if next_node is None:
                print(f"[Debug] Could not find node with ID {next_node_id}")
                break

            # Highlight the next node that just started
            self._loop_controller.node_started.emit(next_node.id)

            # Call process() on the next node (DelayNode will sleep here)
            if isinstance(next_node, DelayNode):
                next_node.process(stop_event=stop_event)
            else:
                next_node.process()

            if stop_event.is_set():
                return
            
            # Move forward
            current_node = next_node

            # If we’ve reached an EndNode, stop the inner loop
            if isinstance(current_node, EndNode):
                break

        if isinstance(current_node, EndNode):
            end_id = current_node.id
            if current_node.get_property('repeat') == 'Single':
                # Emit a “clear” for this end node (and its backdrop), then stop loop
                self._loop_controller.node_started.emit(f"clear:{end_id}")
                stop_event.set()

        # 4) We’ve either hit an EndNode or there were no further connections.
        #    Emit the loop‐finished signal for this StartNode:
        self._loop_controller.loop_iteration_finished.emit(start_id)

        # 5) Immediately loop back to Start, unless stop_event was set
        if stop_event.is_set():
            break

    print(f"[LoopWorker-{start_id}] Thread terminating.")