import sys
import threading
import time
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QDockWidget,
    QToolBar,
    QMessageBox,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPointF, Signal, QObject
from NodeGraphQt import (
    NodeGraph,
    BaseNode,
    PropertiesBinWidget,
    NodesPaletteWidget,
)

# ──────────────────────────────────────────────────────────────────────────────
# 1) Define “global” list of key names for KeyboardNode’s drop‐down.
# ──────────────────────────────────────────────────────────────────────────────
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


# ──────────────────────────────────────────────────────────────────────────────
# 2) Define custom nodes: StartNode, EndNode, DelayNode, KeyboardNode, MouseNode.
# ──────────────────────────────────────────────────────────────────────────────
class StartNode(BaseNode):
    """
    “Start” node: no properties.
    Fires the loop when PLAY is pressed.
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Start'

    def __init__(self):
        super(StartNode, self).__init__()
        # Only an output socket (since “Start” sends its signal out)
        self.add_output('out')

    def process(self, **kwargs):
        """
        In a real engine, this would “emit” the start‐signal.
        Here it’s stubbed.
        """
        print(f"[StartNode: {self.id}] Fired.")


class EndNode(BaseNode):
    """
    “End” node: no properties.
    When a loop reaches this node, it will return to its Start node.
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'End'

    def __init__(self):
        super(EndNode, self).__init__()
        # Only an input socket (since “End” receives a signal)
        self.add_input('in')

    def process(self, **kwargs):
        """
        In a real engine, this would mark the loop’s end and signpost a return to Start.
        Here it’s stubbed.
        """
        print(f"[EndNode: {self.id}] Reached.")


class DelayNode(BaseNode):
    """
    “Delay” node: pauses execution for a given number of milliseconds.
      • delay: Text input (ms to pause)
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Delay'

    def __init__(self):
        super(DelayNode, self).__init__()
        # One input and one output socket
        self.add_input('in')
        self.add_output('out')

        # Numeric field as text; convert to int during process()
        self.add_text_input('delay', 'Delay (ms)')
        self.set_property('delay', '1000')

    def process(self, **kwargs):
        """
        Sleep for the specified number of milliseconds.
        """
        try:
            ms = int(self.get_property('delay'))
        except ValueError:
            ms = 0
        seconds = ms / 1000.0
        print(f"[DelayNode: {self.id}] Sleeping for {ms} ms → {seconds:.3f} seconds.")
        time.sleep(seconds)


class KeyboardNode(BaseNode):
    """
    “Keyboard” action node:
      • key:      Combo (drop‐down of KEY_NAMES)
      • modifier: Combo (None / Ctrl / Alt / Shift)
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
        # Drop‐down for modifier keys
        self.add_combo_menu('modifier', 'Modifier', ['None', 'Ctrl', 'Alt', 'Shift'])
        # Duration (ms) as text
        self.add_text_input('duration', 'Duration (ms)')

        # Defaults
        self.set_property('key', 'Enter')
        self.set_property('modifier', 'None')
        self.set_property('duration', '100')

    def process(self, **kwargs):
        key = self.get_property('key')
        modifier = self.get_property('modifier')
        try:
            ms = int(self.get_property('duration'))
        except ValueError:
            ms = 0
        print(f"[KeyboardNode: {self.id}] Key='{key}', Modifier='{modifier}', Duration={ms}ms")
        # In a real implementation, you might do:
        #    if modifier != 'None': keyboard.press(modifier.lower())
        #    keyboard.press_and_release(key.lower())
        #    if modifier != 'None': keyboard.release(modifier.lower())
        time.sleep(ms / 1000.0)


class MouseNode(BaseNode):
    """
    “Mouse” action node:
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
        self.add_combo_menu('button', 'Button', ['Left', 'Right', 'Middle'])
        self.add_text_input('hold', 'Hold Time (ms)')

        # Defaults
        self.set_property('x', '0')
        self.set_property('y', '0')
        self.set_property('button', 'Left')
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
        # In a real implementation, you might use:
        #    pyautogui.mouseDown(x, y, button=button.lower())
        #    time.sleep(ms/1000.0)
        #    pyautogui.mouseUp(x, y, button=button.lower())
        time.sleep(ms / 1000.0)


# ──────────────────────────────────────────────────────────────────────────────
# 3) Simple signals for thread control
# ──────────────────────────────────────────────────────────────────────────────
class LoopController(QObject):
    """
    A small QObject to emit signals when loops start/stop.
    """
    # Signal emitted when a loop (for a given Start node ID) has ended one iteration.
    loop_iteration_finished = Signal(str)


# ──────────────────────────────────────────────────────────────────────────────
# 4) Main Application: QMainWindow with NodeGraph at the center, two docks,
#    plus a toolbar (Play | Pause | Stop) and a threaded loop “engine.”
# ──────────────────────────────────────────────────────────────────────────────
class AutomationDesigner(QMainWindow):
    def __init__(self):
        super(AutomationDesigner, self).__init__()

        self.setWindowTitle('Automation Designer')
        self.resize(1200, 800)

        # 4.1) Create the NodeGraph and register node types:
        self._graph = NodeGraph()
        self._graph.register_node(StartNode)
        self._graph.register_node(EndNode)
        self._graph.register_node(DelayNode)
        self._graph.register_node(KeyboardNode)
        self._graph.register_node(MouseNode)

        # 4.2) Set the NodeGraph’s central widget:
        self.setCentralWidget(self._graph.widget)

        # 4.3) Add a “Properties” dock on the right:
        self._properties_bin = PropertiesBinWidget(node_graph=self._graph)
        properties_dock = QDockWidget('Properties', self)
        properties_dock.setWidget(self._properties_bin)
        properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)

        # 4.4) Add a “Nodes Palette” dock on the left:
        self._nodes_palette = NodesPaletteWidget(node_graph=self._graph)
        palette_dock = QDockWidget('Nodes Palette', self)
        palette_dock.setWidget(self._nodes_palette)
        palette_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, palette_dock)

        # 4.5) Grab the QGraphicsView (the canvas) to intercept right‐click:
        self._view = self._graph.viewer()
        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.customContextMenuRequested.connect(self._show_context_menu)

        # 4.6) Remember the last scene position (for placing new nodes):
        self._last_scene_pos = QPointF(0, 0)

        # 4.7) Build the top toolbar with Play | Pause | Stop:
        self._build_toolbar()

        # 4.8) Prepare loop control structures:
        #      _loop_threads maps Start node ID (string) → threading.Thread
        #      _loop_stop_flags maps Start node ID → threading.Event (to signal stop)
        #      _loop_pause_flags maps Start node ID → threading.Event (to signal pause)
        self._loop_threads = {}
        self._loop_stop_flags = {}
        self._loop_pause_flags = {}

        # 4.9) A signal emitter if you need to hook back to the GUI when a loop iteration finishes:
        self._loop_controller = LoopController()
        self._loop_controller.loop_iteration_finished.connect(self._on_loop_iteration_finished)

        # 4.10) Finally, show the NodeGraph’s window:
        self._graph.show()

    # ──────────────────────────────────────────────────────────────────────────
    # 4.7) Build toolbar with Play, Pause, Stop
    # ──────────────────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        toolbar = QToolBar("Controls", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Play button
        self._play_action = QAction("Play", self)
        self._play_action.triggered.connect(self._on_play)
        toolbar.addAction(self._play_action)

        # Pause button
        self._pause_action = QAction("Pause", self)
        self._pause_action.triggered.connect(self._on_pause)
        toolbar.addAction(self._pause_action)

        # Stop button
        self._stop_action = QAction("Stop", self)
        self._stop_action.triggered.connect(self._on_stop)
        toolbar.addAction(self._stop_action)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.5) Canvas right‐click context menu
    # ──────────────────────────────────────────────────────────────────────────
    def _show_context_menu(self, view_pos):
        """
        Called when the user right‐clicks on the canvas.
        Pop up a menu: Add Node → {Start, End, Delay, Keyboard, Mouse}.
        """
        # Convert VIEW coords → SCENE coords so new node appears where clicked:
        self._last_scene_pos = self._view.mapToScene(view_pos)

        # Build the context menu
        menu = QMenu()
        add_menu = menu.addMenu('Add Node')

        # Add each node type
        for node_label in ['Start', 'End', 'Delay', 'Keyboard', 'Mouse']:
            action = add_menu.addAction(node_label)
            action.triggered.connect(lambda checked=False, nl=node_label: self._create_node(nl))

        # Show at the global position
        menu.exec(self._view.mapToGlobal(view_pos))

    # ──────────────────────────────────────────────────────────────────────────
    # 4.6) Create + place a node by label
    # ──────────────────────────────────────────────────────────────────────────
    def _create_node(self, node_label):
        """
        Instantiate a node by its label and add it to the graph at the last click position.
        """
        node_map = {
            'Start': StartNode,
            'End': EndNode,
            'Delay': DelayNode,
            'Keyboard': KeyboardNode,
            'Mouse': MouseNode
        }
        NodeClass = node_map.get(node_label)
        if NodeClass is None:
            return

        new_node = NodeClass()
        self._graph.add_node(new_node)
        new_node.set_pos(self._last_scene_pos.x(), self._last_scene_pos.y())

    # ──────────────────────────────────────────────────────────────────────────
    # 4.8) PLAY, PAUSE, STOP handlers
    # ──────────────────────────────────────────────────────────────────────────
    def _on_play(self):
        """
        Called when the user clicks ‘Play’.  
        For each Start node in the graph:
          • If it’s not already running, spawn a thread to run its loop.
        """
        # Find all StartNode instances using all_nodes()
        all_nodes = self._graph.all_nodes()
        start_nodes = [n for n in all_nodes if isinstance(n, StartNode)]

        if not start_nodes:
            QMessageBox.warning(self, "No Start Node", "Please add at least one Start node before playing.")
            return

        for start_node in start_nodes:
            start_id = start_node.id  # <-- use the attribute, not a call
            # If there’s no running thread for this Start node, launch one
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

    def _on_pause(self):
        """
        Called when the user clicks ‘Pause’.  
        This sets the pause flag for all running loops.
        """
        for start_id, pause_event in self._loop_pause_flags.items():
            pause_event.set()
        print("[Main] All loops paused. (will resume when Play is clicked again)")

    def _on_stop(self):
        """
        Called when the user clicks ‘Stop’.  
        This sets the stop flag for all running loops, and clears pause flags.
        """
        for start_id, stop_event in self._loop_stop_flags.items():
            stop_event.set()
        # Clear pause flags as well
        for start_id, pause_event in self._loop_pause_flags.items():
            pause_event.clear()
        print("[Main] All loops stopped.")

    # ──────────────────────────────────────────────────────────────────────────
    # 4.9) Loop worker function (runs in its own thread per Start node)
    # ──────────────────────────────────────────────────────────────────────────
    def _run_loop(self, start_node, stop_event: threading.Event, pause_event: threading.Event):
        """
        Very simplified “loop”:
          1. While not stop_event.is_set():
               a. If pause_event.is_set(): wait until it’s cleared (i.e. Play clicked again).
               b. Traverse from start_node → … → End node, calling process() on each.
               c. When an End node is reached, emit a signal and immediately jump back to Start.
        """
        start_id = start_node.id  # <-- attribute, not a call
        print(f"[LoopWorker-{start_id}] Thread started.")

        while not stop_event.is_set():
            # 1) Handle Pause: if pause_event is set, wait in small increments
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)

            if stop_event.is_set():
                break

            # 2) “Fire” the Start node
            start_node.process()

            # 3) Walk the graph from this Start node until we hit an End node.
            #    (***SUBSTITUTE IN REAL TRAVERSAL LOGIC HERE***)
            #    For now, simply sleep a bit and then “hit” every End node we find.
            time.sleep(0.2)  # simulate time spent in between nodes

            # Call process() on all End nodes (placeholder)
            all_nodes = self._graph.all_nodes()
            end_nodes = [n for n in all_nodes if isinstance(n, EndNode)]
            for end_node in end_nodes:
                if stop_event.is_set():
                    break
                end_node.process()

            # 4) Notify that one iteration of this loop is finished
            self._loop_controller.loop_iteration_finished.emit(start_id)

            # 5) Immediately loop back to Start, unless stop_event was set
            if stop_event.is_set():
                break

        print(f"[LoopWorker-{start_id}] Thread terminating.")

    # ──────────────────────────────────────────────────────────────────────────
    # 4.10) Receive a signal when each loop iteration finishes
    # ──────────────────────────────────────────────────────────────────────────
    def _on_loop_iteration_finished(self, start_id: str):
        """
        Called in the GUI thread whenever a loop iteration completes for a Start node.
        You can use this signal to update a UI counter, log, or visual indicator.
        """
        print(f"[Main] Loop iteration finished for Start Node {start_id}.")


# ──────────────────────────────────────────────────────────────────────────────
# 5) Bootstrap the QApplication
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutomationDesigner()
    window.show()
    sys.exit(app.exec())
