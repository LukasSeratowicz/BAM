# nodes/KeyboardNode.py

from NodeGraphQt import (
    BaseNode,
)
import time
from pynput.keyboard import Controller as KeyboardController

KEY_NAMES = [
    'None',
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'Enter', 'Space', 'Tab', 'Esc',
    'Shift', 'Ctrl', 'Alt',
    'Up', 'Down', 'Left', 'Right',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
]

keyboard = KeyboardController()

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
        self.add_combo_menu('key', 'Key', KEY_NAMES)

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
      
    def copy(self):
        new_node = KeyboardNode()
        for prop_name, _ in self.properties().items():
            if prop_name in ('inputs', 'outputs', 'id'):
                continue
            try:
                new_node.set_property(prop_name, self.get_property(prop_name))
            except Exception:
                pass

        pos = self.pos()
        try:
            x, y = pos.x(), pos.y()
        except AttributeError:
            x, y = pos[0], pos[1]
        new_node.set_pos(x + 20, y + 20)

        return new_node
