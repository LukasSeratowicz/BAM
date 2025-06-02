# shared/globals.py

def init():
    global version
    global hard_start, hard_stop
    global show_coords, mouse_x, mouse_y

    version = "0.1.7alpha"

    hard_start  = False
    hard_stop   = False

    show_coords = False
    mouse_x     = 0
    mouse_y     = 0

_initialized = False

def ensure_initialized():
    global _initialized
    if not _initialized:
        init()
        _initialized = True
