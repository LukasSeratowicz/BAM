# handlers/MouseListener.py

from pynput.mouse import Listener as MouseListener

def on_move(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y
    
mouseListener = MouseListener(on_move=on_move)