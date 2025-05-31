import sys
import os
import json
import threading
import time
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QDockWidget,
    QToolBar,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtGui import QAction, QKeyEvent
from PySide6.QtCore import Qt, QPointF, Signal, QObject
from NodeGraphQt import (
    NodeGraph,
    BaseNode,
    PropertiesBinWidget,
    NodesPaletteWidget,
)
import PySide6
import NodeGraphQt

print(f"--- My Automation App Environment ---")
print(f"Python version: {sys.version}")
print(f"PySide6 version: {PySide6.__version__}")
print(f"Qt version used by PySide6: {PySide6.QtCore.qVersion()}")
print(f"NodeGraphQt version: {NodeGraphQt.__version__}")
print("------------------------------------")

from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Listener, Key

keyboard = KeyboardController()
mouse = MouseController()

hard_stop = False

def on_press(key):
    try:
        if key == Key.f1:
            print("F1 key pressed!")
    except AttributeError:
        pass

def on_release(key):
    global hard_stop
    if key == Key.f1:
        hard_stop = True
    
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

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

mouse_button_map = {
    "Left": Button.left,
    "Right": Button.right,
    "Center": Button.middle,
    "Mouse4": Button.x1,  # Side button 1
    "Mouse5": Button.x2,  # Side button 2
}


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
        Here it’s stubbed just to show the ID.
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
        In a real engine, this would mark the loop’s end.
        Here it’s stubbed just to show the ID.
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

        # Numeric field as text (we chunk it in process() for responsive pause/stop)
        self.add_text_input('delay', 'Delay (ms)')
        self.set_property('delay', '1000')

    def process(self, **kwargs):
        """
        Sleep for the specified number of milliseconds, in 100ms chunks,
        printing status each chunk so you see the delay happening.
        """
        try:
            ms_total = int(self.get_property('delay'))
        except ValueError:
            ms_total = 0

        print(f"[DelayNode: {self.id}] Beginning {ms_total} ms delay.")
        # Break into 100ms increments so we can see progress and respect stop/pause.
        ms_done = 0
        while ms_done < ms_total:
            chunk = min(100, ms_total - ms_done)
            time.sleep(chunk / 1000.0)
            ms_done += chunk
            #print(f"[DelayNode: {self.id}] still sleeping... {ms_done}/{ms_total} ms")
        print(f"[DelayNode: {self.id}] Completed delay.")


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

        button_to_click = mouse_button_map.get(button)

        if button_to_click:
            mouse.position = (x, y)
            mouse.press(button_to_click)
            time.sleep(ms / 1000.0)
            mouse.release(button_to_click)
        else:
            print(f"Button '{button}' not recognized")
            

# ──────────────────────────────────────────────────────────────────────────────
# 3) Simple signals for thread control
# ──────────────────────────────────────────────────────────────────────────────
class LoopController(QObject):
    loop_iteration_finished = Signal(str)


# ──────────────────────────────────────────────────────────────────────────────
# 4) Main Application: QMainWindow with NodeGraph at the center, two docks,
#    plus a toolbar (Play | Pause | Stop) and a threaded loop “engine.”
# ──────────────────────────────────────────────────────────────────────────────
class AutomationDesigner(QMainWindow):
    DEFAULT_GRAPH_FILE = "autosave_graph.json"
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

        # # 4.3) Add a “Properties” dock on the right:
        # self._properties_bin = PropertiesBinWidget(node_graph=self._graph)
        # properties_dock = QDockWidget('Properties', self)
        # properties_dock.setWidget(self._properties_bin)
        # properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)

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
        self._build_file_menu()

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
        self._on_load(file_path=self.DEFAULT_GRAPH_FILE)




    def keyPressEvent(self, event: QKeyEvent):
        # Check for Delete or Backspace key
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            selected_nodes = self._graph.selected_nodes()
            if selected_nodes:
                confirm = QMessageBox.question(self, "Delete Nodes",
                                            f"Are you sure you want to delete {len(selected_nodes)} selected node(s)?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    for node in selected_nodes:
                        self._graph.remove_node(node)
                    print(f"Deleted {len(selected_nodes)} node(s).")
                    self.saveGraphs()
                event.accept()
                return
        super(AutomationDesigner, self).keyPressEvent(event)
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
    # Save/Load handlers
    # ──────────────────────────────────────────────────────────────────────────
    def _on_new_graph(self):
        """
        Clears the current graph and stops all running loops.
        """
        reply = QMessageBox.question(self, "New Graph",
                                    "Are you sure you want to create a new graph? Any unsaved changes will be lost.",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._on_stop() # Stop any running loops first
            self._clear_all_nodes_fallback()
            print("[Main] New graph created.")

    def _on_save(self):
        """
        Saves the current graph to a JSON file.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph",
                                                 self.DEFAULT_GRAPH_FILE,
                                                 "Graph Files (*.json);;All Files (*)")
        if file_path:
            try:
                graph_data = self._graph.serialize_session()

                # 2. Manually write the dictionary to the specified JSON file
                with open(file_path, 'w') as f:
                    json.dump(graph_data, f, indent=4) # Using indent for readability in the JSON file

                print(f"[Main] Graph saved to: {file_path}")
                # Optionally, update DEFAULT_GRAPH_FILE for next auto-save/load
                self.DEFAULT_GRAPH_FILE = file_path
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save graph: {e}")
                print(f"[Main] Failed to save graph: {e}")


    def _clear_all_nodes_fallback(self):
        """
        A fallback method to clear all nodes by iterating and removing them one by one.
        This is used if standard methods like clear_nodes() or remove_all_nodes() are not available.
        """
        # It's important to convert to a list because you're modifying the collection
        # while iterating. If you don't, you'll get a RuntimeError for changing size during iteration.
        for node in list(self._graph.all_nodes()):
            self._graph.remove_node(node)
        print("[Main] All nodes cleared using fallback method.")

    def _on_load(self, file_path=None):
        """
        Loads a graph from a JSON file. If file_path is None, a file dialog opens.
        """
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Graph",
                                                    self.DEFAULT_GRAPH_FILE,
                                                    "Graph Files (*.json);;All Files (*)")
        if file_path and os.path.exists(file_path): # Check if file exists for auto-load
            self._on_stop() # Stop any running loops before loading a new graph
            try:
                # IMPORTANT: Before deserializing, you should clear existing nodes
                # and ensure all custom node classes are registered (which you already do in __init__).
                self._clear_all_nodes_fallback()

                # CHANGED: Read the JSON file content into a dictionary
                with open(file_path, 'r') as f:
                    graph_data = json.load(f)

                # Deserialize the graph from the file
                self._graph.deserialize_session(graph_data)
                print(f"[Main] Graph loaded from: {file_path}")
                # Optionally, update DEFAULT_GRAPH_FILE for next auto-save/load
                self.DEFAULT_GRAPH_FILE = file_path
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load graph: {e}\n"
                                    "Please ensure node classes are registered.")
                print(f"[Main] Failed to load graph: {e}")
        elif file_path: # If file_path was provided but didn't exist (e.g., first launch)
            print(f"[Main] No graph file found at '{file_path}'. Starting with empty canvas.")
        else: # User cancelled file dialog
            print("[Main] Load operation cancelled.")

    def saveGraphs(self):
        try:
            graph_data = self._graph.serialize_session()

            with open(self.DEFAULT_GRAPH_FILE, 'w') as f:
                json.dump(graph_data, f, indent=4)

            print(f"[Main] Auto-saved graph to: {self.DEFAULT_GRAPH_FILE}")
        except Exception as e:
            print(f"[Main] Failed to auto-save graph on exit: {e}")

    def closeEvent(self, event):
        self._on_stop()
        # Auto-save the current graph
        self.saveGraphs() # Save the current graph before closing

        listener.stop() # Stop pynput listener
        listener.join() # Wait for listener thread to finish
        super().closeEvent(event)
        event.accept()

    # ──────────────────────────────────────────────────────────────────────────
    # 4.8) Build File menu with New, Open, Save, Exit
    # ──────────────────────────────────────────────────────────────────────────
    def _build_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # New Action
        new_action = QAction("New Graph", self)
        new_action.triggered.connect(self._on_new_graph)
        file_menu.addAction(new_action)

        # Open Action
        open_action = QAction("Open Graph...", self)
        open_action.triggered.connect(lambda: self._on_load()) # No default file path
        file_menu.addAction(open_action)

        # Save Action
        save_action = QAction("Save Graph...", self)
        save_action.triggered.connect(self._on_save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Exit Action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.5) Canvas right‐click context menu
    # ──────────────────────────────────────────────────────────────────────────
    def _show_context_menu(self, view_pos):
        """
        Called when the user right-clicks on the canvas.
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
        Proper graph traversal for a simple chain:
          1. While not stopped:
               a. Wait if paused.
               b. Call start_node.process().
               c. Walk connections: from Start → next node → next → … until we hit an EndNode.
                   • At each node, call node.process(). DelayNode.process() will sleep.
               d. Once we hit an EndNode, emit a “loop iteration finished” signal.
               e. Loop back to Start (unless stopped).
        """
        start_id = start_node.id
        print(f"[LoopWorker-{start_id}] Thread started.")

        while not stop_event.is_set():
            # 1) Handle Pause: if pause_event is set, wait until it’s cleared
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)

            if stop_event.is_set():
                break

            global hard_stop
            if hard_stop:
                print(f"[LoopWorker-{start_id}] Hard stop triggered, exiting loop.")
                hard_stop = False
                break

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
                out_port = outputs[port_names[0]]

                # See which ports are connected
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

                # Call process() on the next node (DelayNode will sleep here)
                next_node.process()

                # Move forward
                current_node = next_node

                # If we’ve reached an EndNode, stop the inner loop
                if isinstance(current_node, EndNode):
                    break

            # 4) We’ve either hit an EndNode or there were no further connections.
            #    Emit the loop‐finished signal for this StartNode:
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
