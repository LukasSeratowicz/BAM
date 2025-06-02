# AutomationDesigner/ShowContextMenuHandler.py

from PySide6.QtWidgets import QMenu

def showContextMenuHandler(self, view_pos):
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