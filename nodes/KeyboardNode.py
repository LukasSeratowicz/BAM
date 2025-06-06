# nodes/KeyboardNode.py

import shared.globals as g

from NodeGraphQt import BaseNode
import time
from pynput.keyboard import Controller as KeyboardController
from pynput import keyboard

_PYNPUT_SPECIAL_KEY_TO_STRING_MAP = {
    # Function Keys (F1-F3 are global hotkeys for start/stop/show coords)
    keyboard.Key.f4: 'F4', keyboard.Key.f5: 'F5', keyboard.Key.f6: 'F6',
    keyboard.Key.f7: 'F7', keyboard.Key.f8: 'F8', keyboard.Key.f9: 'F9',
    keyboard.Key.f10: 'F10', keyboard.Key.f11: 'F11', keyboard.Key.f12: 'F12',

    # Standard Action/Navigation Keys
    keyboard.Key.enter: 'Enter',
    keyboard.Key.space: 'Space',
    keyboard.Key.tab: 'Tab',
    keyboard.Key.esc: 'Esc',
    keyboard.Key.backspace: 'Backspace',
    keyboard.Key.delete: 'Delete',
    keyboard.Key.insert: 'Insert',
    keyboard.Key.home: 'Home',
    keyboard.Key.end: 'End',
    keyboard.Key.page_up: 'PageUp',
    keyboard.Key.page_down: 'PageDown',

    # Arrow Keys
    keyboard.Key.up: 'Up', keyboard.Key.down: 'Down',
    keyboard.Key.left: 'Left', keyboard.Key.right: 'Right',

    # Modifier Keys
    keyboard.Key.shift: 'Shift', keyboard.Key.shift_l: 'Shift', keyboard.Key.shift_r: 'Shift',
    keyboard.Key.ctrl: 'Ctrl', keyboard.Key.ctrl_l: 'Ctrl', keyboard.Key.ctrl_r: 'Ctrl',
    keyboard.Key.alt: 'Alt', keyboard.Key.alt_l: 'Alt', keyboard.Key.alt_r: 'Alt',
    # keyboard.Key.alt_gr: 'AltGr',
    keyboard.Key.cmd: 'Meta', keyboard.Key.cmd_l: 'Meta', keyboard.Key.cmd_r: 'Meta', # Windows/Command key

    keyboard.Key.caps_lock: 'CapsLock',
    keyboard.Key.num_lock: 'NumLock',
    keyboard.Key.scroll_lock: 'ScrollLock',

    # Special Purpose
    keyboard.Key.print_screen: 'PrintScreen',
    keyboard.Key.pause: 'Pause',
    keyboard.Key.menu: 'Menu',
    # keyboard.Key.sys_req: 'SysReq',

    # Multimedia keys
    keyboard.Key.media_volume_up: 'VolumeUp',
    keyboard.Key.media_volume_down: 'VolumeDown',
    keyboard.Key.media_volume_mute: 'VolumeMute',
    keyboard.Key.media_play_pause: 'MediaPlay',
    #keyboard.Key.media_stop: 'MediaStop',
    keyboard.Key.media_previous: 'MediaPrevious',
    keyboard.Key.media_next: 'MediaNext',
}

_KEYPAD_KEY_CODES_TO_STRING_MAP = {
    96: 'Num0',  # Numpad 0
    97: 'Num1',  # Numpad 1
    98: 'Num2',  # Numpad 2
    99: 'Num3',  # Numpad 3
    100: 'Num4', # Numpad 4
    101: 'Num5', # Numpad 5
    102: 'Num6', # Numpad 6
    103: 'Num7', # Numpad 7
    104: 'Num8', # Numpad 8
    105: 'Num9', # Numpad 9
    110: 'Num.', # Numpad .   # for some reason, this is not in the Pynput map
}

_STRING_TO_PYNPUT_KEY_MAP = {v: k for k, v in _PYNPUT_SPECIAL_KEY_TO_STRING_MAP.items()}
_STRING_TO_KEYPAD_VK_MAP = {v: k for k, v in _KEYPAD_KEY_CODES_TO_STRING_MAP.items()}

kb_controller = KeyboardController()

class KeyboardNode(BaseNode):
    """
    “Keyboard” action node:
      • key:      Combo (drop‐down of KEY_NAMES)
      • duration: Text input (ms to hold)
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Keyboard'

    def __init__(self):
        super(KeyboardNode, self).__init__()
        # One input, one output socket
        self.add_input('in')
        self.add_output('out')

        # Drop‐down of key names
        self.add_combo_menu('key', 'Key', g._desired_key_strings)

        # Drop‐down of type
        self.add_combo_menu('type', 'Type', ['Press', 'Release', 'Hold'])
        # Duration (ms) as text
        self.add_text_input('duration', 'Duration (ms) [Hold only]')

        # Defaults
        self.set_property('key', 'Enter')
        self.set_property('type', 'Hold')
        self.set_property('duration', '100')

    def process(self, **kwargs):
        key = self.get_property('key')
        type = self.get_property('type')
        try:
            ms = int(self.get_property('duration'))
        except ValueError:
            ms = 0
        print(f"[KeyboardNode: {self.id}] Key='{key}', Duration={ms}ms")

        if type == 'Press':
            keyboard.press(key.lower())
        elif type == 'Release':
            keyboard.release(key.lower())
        elif type == 'Hold':
            keyboard.press(key.lower())
            time.sleep(ms / 1000.0)
            keyboard.release(key.lower())

    def process(self, **kwargs):
        key_str = self.get_property('key')
        action_type = self.get_property('type')
        try:
            ms = int(self.get_property('duration'))
        except (ValueError, TypeError):
            ms = 0
        print(f"[KeyboardNode: {self.id}] Key='{key_str}', Duration={ms}ms")

        if ms < 0:
            print(f"Error: [KeyboardNode] Duration cannot be negative. Received: {ms}ms")
            return
        if key_str == 'None' or key_str is None:
            print(f"Error: [KeyboardNode] Key cannot be 'None'. Received: {key_str}")
            return

        key_to_action = None
        if key_str in _STRING_TO_PYNPUT_KEY_MAP:
            key_to_action = _STRING_TO_PYNPUT_KEY_MAP[key_str]
        elif key_str in _STRING_TO_KEYPAD_VK_MAP:
            vk_code = _STRING_TO_KEYPAD_VK_MAP[key_str]
            key_to_action = keyboard.KeyCode.from_vk(vk_code)
        elif len(key_str) == 1:
            key_to_action = key_str.lower()
        
        if key_to_action is None:
            print(f"Error: [KeyboardNode] Key '{key_str}' is not recognized or supported.")
            return

        if action_type == 'Press':
            kb_controller.press(key_to_action)
        elif action_type == 'Release':
            kb_controller.release(key_to_action)
        elif action_type == 'Hold':
            kb_controller.press(key_to_action)
            if ms > 0:
                time.sleep(ms / 1000.0)
            kb_controller.release(key_to_action)
     
    def copy(self):
        node_pos = self.pos() 
        try:
            orig_x, orig_y = node_pos.x(), node_pos.y()
        except AttributeError: 
            orig_x, orig_y = node_pos[0], node_pos[1]

        props = {}

        try:
            all_prop_keys = list(self.properties().keys())
            for name in all_prop_keys:
                if name not in ('inputs', 'outputs', 'id'):
                    val = self.get_property(name)
                    props[name] = val
        except Exception as e:
            print(f"  [KeyboardNode.copy] ERROR during collection from self.properties(): {e}")

        custom_widget_prop_names = ['key', 'type', 'duration']
        for name in custom_widget_prop_names:
            try:
                val = self.get_property(name) 
                props[name] = val
            except Exception as e:
                print(f"    [KeyboardNode.copy] ERROR collecting explicitly for '{name}': {e}. It will not be copied.")

        return (self.id, self.__class__, props, (orig_x, orig_y))