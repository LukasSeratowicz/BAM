"""
main.py

PySide6 + NodeGraphQt (“nodeeditor”) example with:
  • Right-click → “Add Node” menu (Keyboard / Mouse)
  • Directly instantiating KeyboardNode / MouseNode and adding via graph.add_node(...)
  • Using add_text_input for numeric fields to avoid missing methods
  • QDockWidget used for docking the Properties panel and Nodes Palette
"""

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QDockWidget,
)
from PySide6.QtCore import Qt, QPointF
from NodeGraphQt import (
    NodeGraph,
    BaseNode,
    PropertiesBinWidget,
    NodesPaletteWidget,
)


# ──────────────────────────────────────────────────────────────────────────────
# 1) Define two custom nodes: KeyboardNode and MouseNode.
#    (Use add_text_input(...) for numeric fields + set_property(...))
# ──────────────────────────────────────────────────────────────────────────────
class KeyboardNode(BaseNode):
    """
    “Keyboard” action node:
      • key:      Text input (e.g. 'Enter', 'A', etc.)
      • modifier: Combo (None / Ctrl / Alt / Shift)
      • duration: Text input (ms to hold)  ← user must type a number as string
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Keyboard'

    def __init__(self):
        super(KeyboardNode, self).__init__()

        # 1) Add one input socket and one output socket
        self.add_input('in')
        self.add_output('out')

        # 2) Add properties:
        self.add_text_input('key', 'Key')
        self.add_combo_menu('modifier', 'Modifier', ['None', 'Ctrl', 'Alt', 'Shift'])
        # Use text input for duration (numeric as string)
        self.add_text_input('duration', 'Duration (ms)')

        # 3) Set default values via set_property(property_name, value)
        self.set_property('key', 'Enter')
        self.set_property('modifier', 'None')
        self.set_property('duration', '100')  # stored as string

    def process(self, **kwargs):
        """
        Example of how you could execute this node:
          key      = self.get_property('key')         # e.g. 'Enter'
          modifier = self.get_property('modifier')    # e.g. 'None' or 'Ctrl'
          duration_str = self.get_property('duration')# e.g. '100'
          duration = int(duration_str)

        Then send a keystroke via e.g. `pyautogui` or `keyboard`.
        """
        key = self.get_property('key')
        modifier = self.get_property('modifier')
        try:
            duration = int(self.get_property('duration'))
        except ValueError:
            duration = 0

        # Example placeholder (replace with your actual keystroke library):
        print(f"[KeyboardNode] Sending key='{key}', modifier='{modifier}', duration={duration}ms")


class MouseNode(BaseNode):
    """
    “Mouse” action node:
      • x:         Text input (X coordinate)    ← user must type a number as string
      • y:         Text input (Y coordinate)    ← user must type a number as string
      • button:    Combo (Left / Right / Middle)
      • hold_time: Text input (ms to hold)      ← user must type a number as string
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Mouse'

    def __init__(self):
        super(MouseNode, self).__init__()

        # 1) Add one input socket and one output socket
        self.add_input('in')
        self.add_output('out')

        # 2) Add properties (all numeric fields as text inputs):
        self.add_text_input('x', 'X Coordinate')
        self.add_text_input('y', 'Y Coordinate')
        self.add_combo_menu('button', 'Button', ['Left', 'Right', 'Middle'])
        self.add_text_input('hold_time', 'Hold Time (ms)')

        # 3) Set default values (as strings)
        self.set_property('x', '0')
        self.set_property('y', '0')
        self.set_property('button', 'Left')
        self.set_property('hold_time', '100')

    def process(self, **kwargs):
        """
        Example execution:
          x_str   = self.get_property('x')         # e.g. '0'
          y_str   = self.get_property('y')         # e.g. '0'
          button  = self.get_property('button')    # e.g. 'Left'
          hold_str= self.get_property('hold_time') # e.g. '100'
          x = int(x_str); y = int(y_str); hold = int(hold_str)

        Then perform a click via e.g. `pyautogui`.
        """
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
            hold = int(self.get_property('hold_time'))
        except ValueError:
            hold = 0

        # Example placeholder (replace with your actual mouse-click library):
        print(f"[MouseNode] Clicking at ({x}, {y}) with '{button}' button, hold for {hold}ms")


# ──────────────────────────────────────────────────────────────────────────────
# 2) Main Application: QMainWindow with a NodeGraph at its center and two docks.
# ──────────────────────────────────────────────────────────────────────────────
class AutomationDesigner(QMainWindow):
    def __init__(self):
        super(AutomationDesigner, self).__init__()

        # 2.1) Create the NodeGraph instance:
        self._graph = NodeGraph()

        # Register the node classes so NodeGraphQt knows about them:
        self._graph.register_node(KeyboardNode)
        self._graph.register_node(MouseNode)

        # 2.2) Create the central widget (the node‐editor canvas):
        #      NodeGraph.widget is a QWidget that contains the QGraphicsView.
        self.setCentralWidget(self._graph.widget)
        self.setWindowTitle('Automation Designer')
        self.resize(1000, 700)

        # ────────────────────────────────────────────────────────────────────────
        # 2.3) Create a Properties panel (PropertiesBinWidget) and dock it on the right:
        self._properties_bin = PropertiesBinWidget(node_graph=self._graph)
        properties_dock = QDockWidget('Properties', parent=self)
        properties_dock.setWidget(self._properties_bin)
        properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)

        # 2.4) Create a Nodes Palette (NodesPaletteWidget) and dock it on the left:
        self._nodes_palette = NodesPaletteWidget(node_graph=self._graph)
        palette_dock = QDockWidget('Nodes Palette', parent=self)
        palette_dock.setWidget(self._nodes_palette)
        palette_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, palette_dock)

        # 2.5) Grab the QGraphicsView (canvas) so we can intercept right‐clicks:
        #      NodeGraph.viewer() returns the QGraphicsView.
        self._view = self._graph.viewer()
        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.customContextMenuRequested.connect(self._show_context_menu)

        # 2.6) Store the last scene position (for placing nodes where the user clicked):
        self._last_scene_pos = QPointF(0, 0)

        # 2.7) Finally, show the NodeGraph:
        self._graph.show()

    def _show_context_menu(self, view_pos):
        """
        Called when the user right‐clicks on the canvas.
        Pop up a menu: Add Node → {Keyboard, Mouse}.
        view_pos is in VIEW (QGraphicsView) coordinates.
        """
        # Convert VIEW coords → SCENE coords:
        self._last_scene_pos = self._view.mapToScene(view_pos)

        # Build the context menu:
        menu = QMenu()
        add_menu = menu.addMenu('Add Node')

        # Keyboard action:
        action_keyboard = add_menu.addAction('Keyboard')
        action_keyboard.triggered.connect(lambda: self._create_node('Keyboard'))

        # Mouse action:
        action_mouse = add_menu.addAction('Mouse')
        action_mouse.triggered.connect(lambda: self._create_node('Mouse'))

        # Show the menu at the global screen position (use exec(), not exec_()):
        menu.exec(self._view.mapToGlobal(view_pos))

    def _create_node(self, node_type):
        """
        Create a node of type 'Keyboard' or 'Mouse' at the last clicked scene position.
        Instead of using create_node("Automation.Keyboard"), we directly instantiate
        the class and add it to the graph via graph.add_node(...).
        """
        if node_type == 'Keyboard':
            new_node = KeyboardNode()
        elif node_type == 'Mouse':
            new_node = MouseNode()
        else:
            return

        # Add the newly created node instance to the graph:
        self._graph.add_node(new_node)

        # Place it where the user right‐clicked:
        new_node.set_pos(self._last_scene_pos.x(), self._last_scene_pos.y())


# ──────────────────────────────────────────────────────────────────────────────
# 3) Run the application
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = AutomationDesigner()
    window.show()
    sys.exit(app.exec())
