# AutomationDesigner/KeyPressEventHandler.py

import shared.globals as g

import threading
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

def _get_key_string_from_event(event: QKeyEvent) -> str | None:
    qt_key = event.key()
    modifiers = event.modifiers()

    # Do not trigger on key combinations with Ctrl/Alt unless the key itself is a modifier
    is_standard_shortcut_modifier_active = bool(modifiers & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier))
    
    key_str_from_map = g._QT_KEY_TO_STRING_MAP.get(qt_key)

    if not key_str_from_map or key_str_from_map == 'None':
        return None

    # Case 1: Configured trigger IS 'Ctrl', 'Alt', or 'Shift' (pressed ALONE)
    if key_str_from_map in ['Shift', 'Ctrl', 'Alt']:
        expected_modifier_alone = {
            'Shift': Qt.ShiftModifier,
            'Ctrl': Qt.ControlModifier,
            'Alt': Qt.AltModifier
        }.get(key_str_from_map)
        if modifiers == expected_modifier_alone and key_str_from_map in g.KEY_NAMES_AVAILABLE:
            return key_str_from_map
    
    # Case 2: Configured trigger is a regular key (e.g., 'C', 'F1')
    # Do not trigger if Ctrl, Alt, or Meta is also pressed.
    if is_standard_shortcut_modifier_active:
        return None

    # If we're here, it's a key press without Ctrl/Alt/Meta (Shift might be present for uppercase)
    if key_str_from_map in g.KEY_NAMES_AVAILABLE:
        return key_str_from_map
            
    # Fallback for text from event.text() if necessary, respecting no Ctrl/Alt/Meta
    text = event.text()
    if text: # Should generally not be needed if _QT_KEY_TO_STRING_MAP is comprehensive
        upper_text = text.upper()
        if upper_text in g.KEY_NAMES_AVAILABLE and len(upper_text) == 1 and upper_text.isalnum():
            return upper_text

    return None

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

def keyPressEventHandler(designer, event: QKeyEvent, StartNode):
    pressed_key_str = _get_key_string_from_event(event)
    
    if pressed_key_str: # No 'None' check needed, _get_key_string filters it
        start_node_triggered = False
        for node in list(designer._graph.all_nodes()): 
            if isinstance(node, StartNode):
                try:
                    if node.get_property('key') == pressed_key_str:
                        _trigger_specific_start_node(designer, node)
                        start_node_triggered = True
                except Exception as e:
                    print(f"Error processing StartNode {node.id} for key trigger: {e}") 
        
        if start_node_triggered:
            event.accept()