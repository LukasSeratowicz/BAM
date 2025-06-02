# AutomationDesigner/BuildFileMenuHandler.py

from PySide6.QtGui import QAction

def buildFileMenuHandler(self):
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