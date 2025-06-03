# AutomationDesigner/KeyPressEventHandler.py

import shared.globals as g

import threading

def _trigger_specific_start_node(designer, start_node_instance_actual):
    node_id = start_node_instance_actual.id
    
    if node_id in designer._loop_threads and designer._loop_threads[node_id].is_alive():
        return

    stop_flag = threading.Event()
    pause_flag = threading.Event() 

    designer._loop_stop_flags[node_id] = stop_flag
    designer._loop_pause_flags[node_id] = pause_flag
    
    thread = threading.Thread(
        target=designer._run_loop, 
        args=(start_node_instance_actual, stop_flag, pause_flag),
        daemon=True 
    )
    designer._loop_threads[node_id] = thread
    thread.start()

def keyPressEventHandler(designer, StartNode):
    if not hasattr(g, 'GLOBAL_KEY_PRESS_STATE'):
        return

    for key_str, is_pressed in g.GLOBAL_KEY_PRESS_STATE.items():
        if is_pressed:
            g.GLOBAL_KEY_PRESS_STATE[key_str] = False

            for node in list(designer._graph.all_nodes()): 
                if isinstance(node, StartNode):
                    try:
                        if node.get_property('key') == key_str:
                            _trigger_specific_start_node(designer, node)
                    except Exception as e:
                        print(f"Error triggering StartNode {node.id} from global poll: {e}")