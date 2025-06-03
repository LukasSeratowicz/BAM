# main.py

import shared.globals as g
g.ensure_initialized()
print("[DEBUG] shared/globals contains:", dir(g))

import sys
import threading
import asyncio

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDockWidget,
    QGraphicsView,
)
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QPointF, QTimer

# monkey patch the QGraphicsScene.setSelectionArea method to handle deviceTransform
from PySide6.QtWidgets import QGraphicsScene
_original_set_selection = QGraphicsScene.setSelectionArea

def _patched_setSelectionArea(self, path, mode, deviceTransform=None):
    if deviceTransform is None:
        _original_set_selection(self, path,
                                Qt.ReplaceSelection,
                                mode)
    else:
        _original_set_selection(self, path,
                                Qt.ReplaceSelection,
                                mode,
                                deviceTransform)
QGraphicsScene.setSelectionArea = _patched_setSelectionArea

from NodeGraphQt import (
    NodeGraph,
    NodesPaletteWidget,
    BackdropNode,
)

# ──────────────────────────────────────────────────────────────────────────────
# NODES
# ──────────────────────────────────────────────────────────────────────────────

from nodes.StartNode import StartNode
from nodes.EndNode import EndNode
from nodes.DelayNode import DelayNode
from nodes.KeyboardNode import KeyboardNode
from nodes.MouseNode import MouseNode

# ──────────────────────────────────────────────────────────────────────────────
# HANDLERS
# ──────────────────────────────────────────────────────────────────────────────

from handlers.Overlay import overlay_update_loop
from handlers.LoopController import LoopController

from handlers.KeyboardListener import keyboardListener
keyboardListener.start()

from handlers.MouseListener import mouseListener
mouseListener.start()

# ──────────────────────────────────────────────────────────────────────────────
# AUTOMATION DESIGNER HANDLERS
# ──────────────────────────────────────────────────────────────────────────────

from AutomationDesigner.DeleteNodeEventHandler import deleteNodeEventHandler
from AutomationDesigner.BuildToolbarHandler import buildToolbarHandler
from AutomationDesigner.OnNewGraphHandler import onNewGraphHandler
from AutomationDesigner.OnSaveHandler import onSaveHandler
from AutomationDesigner.ClearAllNodesFallbackHandler import clearAllNodesFallbackHandler
from AutomationDesigner.OnLoadHandler import onLoadHandler
from AutomationDesigner.SaveGraphsHandler import saveGraphsHandler
from AutomationDesigner.BuildFileMenuHandler import buildFileMenuHandler
from AutomationDesigner.ShowContextMenuHandler import showContextMenuHandler
from AutomationDesigner.CreateNodeHandler import createNodeHandler
from AutomationDesigner.OnPlayHandler import onPlayHandler
from AutomationDesigner.OnPauseHandler import onPauseHandler
from AutomationDesigner.OnStopHandler import onStopHandler
from AutomationDesigner.RunLoopHandler import runLoopHandler
from AutomationDesigner.OnLoopIterationFinishedHandler import onLoopIterationFinishedHandler
from AutomationDesigner.CheckHardStartHandler import checkHardStartHandler
from AutomationDesigner.OnNodeStartedHandler import onNodeStartedHandler
from AutomationDesigner.CopyPasteEventHandler import (
    copyPasteEventHandler,
    copySelectedNodesHandler,
    pasteSelectedNodesHandler,
)
from AutomationDesigner.KeyPressEventHandler import keyPressEventHandler
from AutomationDesigner.HighlightNodeInPathHandler import highlightNodeInPathHandler
from AutomationDesigner.ClearHighlightsForPathHandler import clearHighlightsForPathHandler

# ──────────────────────────────────────────────────────────────────────────────
# STATIC VARIABLES
# ──────────────────────────────────────────────────────────────────────────────
NODE_HIGHLIGHT_COLOR = (34, 47, 61)  # light‐yellow (RGB)
NODE_DEFAULT_COLOR   = (13, 18, 23)  # plain white (RGB)


# ──────────────────────────────────────────────────────────────────────────────
# Main Application: QMainWindow with NodeGraph at the center, dock on the left,
#    plus a toolbar (Play | Pause | Stop) and a threaded loop “engine.”
#    plus a File menu with New, Open, Save, Exit.
# ──────────────────────────────────────────────────────────────────────────────
class AutomationDesigner(QMainWindow):
    DEFAULT_GRAPH_FILE = "autosave_graph.json"
    def __init__(self):
        super(AutomationDesigner, self).__init__()

        title = "BAM " + g.version + "- Big AutoMation by Lucas S. -- github.com/LukasSeratowicz/BAM"
        self.setWindowTitle(title)
        self.resize(1200, 800)

        # 4.1.0) Initialize highlighted nodes and backdrops sets
        self._highlighted_nodes = set()
        self._highlighted_backdrops = set()

        # 4.1.1) Create the NodeGraph and register node types:
        self._graph = NodeGraph()
        self._graph.register_node(StartNode)
        self._graph.register_node(EndNode)
        self._graph.register_node(DelayNode)
        self._graph.register_node(KeyboardNode)
        self._graph.register_node(MouseNode)

        # 4.1.2) Set the NodeGraph’s central widget:
        self.setCentralWidget(self._graph.widget)

        # # 4.1.3) Add a “Properties” dock on the right:
        # self._properties_bin = PropertiesBinWidget(node_graph=self._graph)
        # properties_dock = QDockWidget('Properties', self)
        # properties_dock.setWidget(self._properties_bin)
        # properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # self.addDockWidget(Qt.RightDockWidgetArea, properties_dock)

        # 4.1.4) Add a “Nodes Palette” dock on the left:
        self._nodes_palette = NodesPaletteWidget(node_graph=self._graph)
        palette_dock = QDockWidget('Nodes Palette', self)
        palette_dock.setWidget(self._nodes_palette)
        palette_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, palette_dock)

        # 4.1.5) Grab the QGraphicsView (the canvas) to intercept right‐click:
        self._view = self._graph.viewer()
        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.customContextMenuRequested.connect(self._show_context_menu)
        self._view.setDragMode(QGraphicsView.RubberBandDrag)

        # 4.1.6) Remember the last scene position (for placing new nodes):
        self._last_scene_pos = QPointF(0, 0)

        # 4.1.7) Build the top toolbar with Play | Pause | Stop:
        self._build_toolbar()
        self._build_file_menu()

        # 4.1.8) Prepare loop control structures:
        #      _loop_threads maps Start node ID (string) → threading.Thread
        #      _loop_stop_flags maps Start node ID → threading.Event (to signal stop)
        #      _loop_pause_flags maps Start node ID → threading.Event (to signal pause)
        self._loop_threads = {}
        self._loop_stop_flags = {}
        self._loop_pause_flags = {}

        # 4.1.9) A signal emitter if you need to hook back to the GUI when a loop iteration finishes:
        self._loop_controller = LoopController()
        self._loop_controller.loop_iteration_finished.connect(self._on_loop_iteration_finished)
        self._loop_controller.node_started.connect(self._on_node_started)

        self._last_highlighted_backdrop = None

        # 4.1.10) Finally, show the NodeGraph’s window:
        self._graph.show()
        self._on_load(file_path=self.DEFAULT_GRAPH_FILE)

        # 4.1.11) Add this timer to check hard_start flag every 100ms
        self._hard_start_timer = QTimer(self)
        self._hard_start_timer.timeout.connect(self._check_hard_start)
        self._hard_start_timer.start(33)

        # 4.1.12) Define a clipboard for copy/paste operations:
        self._clipboard = []

        # 4.1.13) Initialize the active paths highlights dictionary:
        self._active_paths_highlights = {}

        

    # ──────────────────────────────────────────────────────────────────────────
    # 4.1) KEY PRESS EVENT HANDLER
    # ──────────────────────────────────────────────────────────────────────────
    def keyPressEvent(self, event: QKeyEvent):
        copyPasteEventHandler(self, event)
        if not event.isAccepted():
            deleteNodeEventHandler(self, event)
        if not event.isAccepted():
            keyPressEventHandler(self, event, StartNode)
        if not event.isAccepted():
            super(AutomationDesigner, self).keyPressEvent(event)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.1.1) Copy/Paste handlers
    # ──────────────────────────────────────────────────────────────────────────    
    def copySelectedNodes(self):
        copySelectedNodesHandler(self)

    def pasteSelectedNodes(self):
        pasteSelectedNodesHandler(self)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.2) Build toolbar with Play, Pause, Stop
    # ──────────────────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        buildToolbarHandler(self)
    
    # ──────────────────────────────────────────────────────────────────────────
    # 4.3) Save/Load/New/Close handlers
    # ──────────────────────────────────────────────────────────────────────────
    def _on_new_graph(self):
        onNewGraphHandler(self)

    def _on_save(self):
        onSaveHandler(self)

    def _clear_all_nodes_fallback(self):
        clearAllNodesFallbackHandler(self)

    def _on_load(self, file_path=None):
        onLoadHandler(self, file_path)

    def saveGraphs(self):
        saveGraphsHandler(self)

    def closeEvent(self, event):
        self._on_stop()
        self.saveGraphs()
        mouseListener.stop()
        keyboardListener.stop()
        mouseListener.join()
        keyboardListener.join()
        super().closeEvent(event)
        event.accept()

    # ──────────────────────────────────────────────────────────────────────────
    # 4.4) Build File menu with New, Open, Save, Exit
    # ──────────────────────────────────────────────────────────────────────────
    def _build_file_menu(self):
        buildFileMenuHandler(self)
    
    # ──────────────────────────────────────────────────────────────────────────
    # 4.5) Canvas right‐click context menu
    # ──────────────────────────────────────────────────────────────────────────
    def _show_context_menu(self, view_pos):
        showContextMenuHandler(self, view_pos)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.6) Create + place a node by label
    # ──────────────────────────────────────────────────────────────────────────
    def _create_node(self, node_label):
        node_map = {
            'Start': StartNode,
            'End': EndNode,
            'Delay': DelayNode,
            'Keyboard': KeyboardNode,
            'Mouse': MouseNode
        }
        createNodeHandler(self, node_label, node_map)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.7) PLAY, PAUSE, STOP handlers
    # ──────────────────────────────────────────────────────────────────────────
    def _on_play(self):
        onPlayHandler(self, NODE_DEFAULT_COLOR, StartNode)

    def _on_pause(self):
        onPauseHandler(self)

    def _on_stop(self):
        onStopHandler(self, NODE_DEFAULT_COLOR, BackdropNode)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.8) Loop worker function (runs in its own thread per Start node)
    # ──────────────────────────────────────────────────────────────────────────
    def _run_loop(self, start_node, stop_event: threading.Event, pause_event: threading.Event):
        runLoopHandler(self, start_node, stop_event, pause_event, EndNode, DelayNode)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.9) Receive a signal when each loop iteration finishes
    # ──────────────────────────────────────────────────────────────────────────
    def _on_loop_iteration_finished(self, start_id: str):
        onLoopIterationFinishedHandler(self, start_id)

        
    # ──────────────────────────────────────────────────────────────────────────
    # 4.10) Check for F1 - hard start
    # ──────────────────────────────────────────────────────────────────────────
    def _check_hard_start(self):
        checkHardStartHandler(self)


    # ──────────────────────────────────────────────────────────────────────────
    # 4.11) Highlight nodes
    # ──────────────────────────────────────────────────────────────────────────
    def _on_node_started(self, msg: str):
        onNodeStartedHandler(self, msg)

    def _highlight_node_in_path(self, loop_start_id: str, node_id_to_highlight: str):
        highlightNodeInPathHandler(self, loop_start_id, node_id_to_highlight, NODE_HIGHLIGHT_COLOR)

    def _clear_highlights_for_path(self, loop_start_id: str):
        clearHighlightsForPathHandler(self, loop_start_id, NODE_DEFAULT_COLOR)


# ──────────────────────────────────────────────────────────────────────────────
# 5) Bootstrap the QApplication
# ──────────────────────────────────────────────────────────────────────────────
from qasync import QEventLoop, asyncSlot
if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Replace default event loop with qasync event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = AutomationDesigner()
    window.show()

    # Start the overlay async task
    loop.create_task(overlay_update_loop())

    with loop:
        sys.exit(loop.run_forever())