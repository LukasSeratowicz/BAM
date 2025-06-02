# handlers/MouseListener.py

import shared.globals as g

from pynput.mouse import Listener as MouseListener

def on_move(x, y):
    g.mouse_x = x
    g.mouse_y = y
    
mouseListener = MouseListener(on_move=on_move)