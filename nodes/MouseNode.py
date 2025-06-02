# nodes/MouseNode.py

from NodeGraphQt import (
    BaseNode,
)
import time
from pynput.mouse import Button, Controller as MouseController

MOUSE_ACTION_MAP = {
    "Left": Button.left,
    "Right": Button.right,
    "Center": Button.middle,
    "Mouse4": Button.x1,  # Side button 1
    "Mouse5": Button.x2,  # Side button 2
}

mouse = MouseController()

class MouseNode(BaseNode):
    """
    "Mouse" action node:
      • x:         Text input (X coord)
      • y:         Text input (Y coord)
      • button:    Combo (Left / Right / Middle)
      • hold:      Text input (ms to hold)
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Mouse'

    def __init__(self):
        super(MouseNode, self).__init__()
        # One input, one output socket
        self.add_input('in')
        self.add_output('out')

        # Numeric coords as text inputs
        self.add_text_input('x', 'X Coordinate')
        self.add_text_input('y', 'Y Coordinate')
        self.add_combo_menu('button', 'Button', ['Move', 'Left', 'Right', 'Middle'])
        self.add_text_input('hold', 'Hold Time (ms)')

        # Defaults
        self.set_property('x', '0')
        self.set_property('y', '0')
        self.set_property('button', 'Move')
        self.set_property('hold', '100')

    def process(self, **kwargs):
        try:
            x = int(self.get_property('x'))
        except ValueError:
            x = 0
        try:
            y = int(self.get_property('y'))
        except ValueError:
            y = 0
        button = self.get_property('button')
        try:
            ms = int(self.get_property('hold'))
        except ValueError:
            ms = 0
        print(f"[MouseNode: {self.id}] Clicking at ({x}, {y}) with '{button}', hold {ms}ms")

        if button == 'Move':
            mouse.position = (x, y)
            return

        button_to_click = MOUSE_ACTION_MAP.get(button)

        if button_to_click:
            mouse.position = (x, y)
            mouse.press(button_to_click)
            time.sleep(ms / 1000.0)
            mouse.release(button_to_click)
        else:
            print(f"Button '{button}' not recognized")

    def copy(self):
        new_node = MouseNode()
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