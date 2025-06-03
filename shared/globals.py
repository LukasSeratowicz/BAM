# shared/globals.py

_initialized = False
version = ""
hard_start = False
hard_stop = False
show_coords = False 
mouse_x = 0
mouse_y = 0

_desired_key_strings = []       
KEY_NAMES_AVAILABLE = []        
GLOBAL_KEY_PRESS_STATE = {}


def init():
    global version
    global hard_start, hard_stop
    global show_coords, mouse_x, mouse_y
    global _desired_key_strings
    global KEY_NAMES_AVAILABLE
    global GLOBAL_KEY_PRESS_STATE

    version = "0.1.7alpha"

    hard_start  = False
    hard_stop   = False

    show_coords = False
    mouse_x     = 0
    mouse_y     = 0

    _desired_key_strings = [
        # Alphabetic
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z',

        # Numeric
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',

        # Function Keys
        # 'F1', 'F2', 'F3', # <-- We never use these because F1 - Start all, F2- Stop all, F3 - Overlay
        'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',

        # Standard Action/Navigation Keys
        'Enter', 
        'Space', 'Tab', 'Esc', 'Backspace', 'Delete', 'Insert',
        'Home', 'End', 'PageUp', 'PageDown',

        # Arrow Keys
        'Up', 'Down', 'Left', 'Right',

        # Modifier Keys (if to be used as standalone triggers)
        'Shift', 'Ctrl', 'Alt', 'Meta',
        'CapsLock', 'NumLock', 'ScrollLock',

        # Special Characters
        '-', '=', '[', ']', '\\', ';', "'", '"',
        ',', '.', '/', '`', '+', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
        
        # Numpad Keys (string representations)
        'Num*', 'Num/', 
        'Num+',
        'Num-',
        'Num.',
        'Num0',
        'Num1',
        'Num2',
        'Num3',
        'Num4',
        'Num5',
        'Num6',
        'Num7',
        'Num8',
        'Num9',
        'Num.',
        
        # Multimedia keys
        'VolumeUp', 'VolumeDown', 'VolumeMute', 'MediaPlay',
        'MediaStop', 'MediaPrevious', 'MediaNext',

        # Special Purpose
        'PrintScreen', 'Pause', 'SysReq', 'Help', 'Menu'
    ]

    KEY_NAMES_AVAILABLE = ['None'] + sorted(list(set(_desired_key_strings)))
    
    GLOBAL_KEY_PRESS_STATE = {key_str: False for key_str in _desired_key_strings}



def ensure_initialized():
    global _initialized
    if not _initialized:
        init()
        _initialized = True
