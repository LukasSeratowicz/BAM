# shared/globals.py

from PySide6.QtCore import Qt

def init():
    global version
    global hard_start, hard_stop
    global show_coords, mouse_x, mouse_y
    global key_list
    global _QT_KEY_TO_STRING_MAP, KEY_NAMES_AVAILABLE

    version = "0.1.7alpha"

    hard_start  = False
    hard_stop   = False

    show_coords = False
    mouse_x     = 0
    mouse_y     = 0

    _QT_KEY_TO_STRING_MAP = {
        # Alphabetic
        Qt.Key_A: 'A', Qt.Key_B: 'B', Qt.Key_C: 'C', Qt.Key_D: 'D', Qt.Key_E: 'E',
        Qt.Key_F: 'F', Qt.Key_G: 'G', Qt.Key_H: 'H', Qt.Key_I: 'I', Qt.Key_J: 'J',
        Qt.Key_K: 'K', Qt.Key_L: 'L', Qt.Key_M: 'M', Qt.Key_N: 'N', Qt.Key_O: 'O',
        Qt.Key_P: 'P', Qt.Key_Q: 'Q', Qt.Key_R: 'R', Qt.Key_S: 'S', Qt.Key_T: 'T',
        Qt.Key_U: 'U', Qt.Key_V: 'V', Qt.Key_W: 'W', Qt.Key_X: 'X', Qt.Key_Y: 'Y',
        Qt.Key_Z: 'Z',

        # Numeric
        Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3', Qt.Key_4: '4',
        Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7', Qt.Key_8: '8', Qt.Key_9: '9',

        # Function Keys
        #Qt.Key_F1: 'F1', Qt.Key_F2: 'F2', Qt.Key_F3: 'F3',  <-- We never use these because F1 - Start all, F2- Stop all, F3 - Overlay
        Qt.Key_F4: 'F4', Qt.Key_F5: 'F5', Qt.Key_F6: 'F6', Qt.Key_F7: 'F7', Qt.Key_F8: 'F8',
        Qt.Key_F9: 'F9', Qt.Key_F10: 'F10', Qt.Key_F11: 'F11', Qt.Key_F12: 'F12',

        # Standard Action/Navigation Keys
        Qt.Key_Enter: 'Enter', Qt.Key_Return: 'Enter', 
        Qt.Key_Space: 'Space',
        Qt.Key_Tab: 'Tab',
        Qt.Key_Escape: 'Esc',
        Qt.Key_Backspace: 'Backspace',
        Qt.Key_Delete: 'Delete',
        Qt.Key_Insert: 'Insert',
        Qt.Key_Home: 'Home',
        Qt.Key_End: 'End',
        Qt.Key_PageUp: 'PageUp',
        Qt.Key_PageDown: 'PageDown',

        # Arrow Keys
        Qt.Key_Up: 'Up', Qt.Key_Down: 'Down',
        Qt.Key_Left: 'Left', Qt.Key_Right: 'Right',

        # Modifier Keys
        Qt.Key_Shift: 'Shift',
        Qt.Key_Control: 'Ctrl',         
        Qt.Key_Alt: 'Alt',              
        Qt.Key_Meta: 'Meta', #Windows/Command key
        Qt.Key_CapsLock: 'CapsLock',
        Qt.Key_NumLock: 'NumLock',
        Qt.Key_ScrollLock: 'ScrollLock',

        # Special Characters
        Qt.Key_Minus: '-', Qt.Key_Equal: '=',
        Qt.Key_BracketLeft: '[', Qt.Key_BracketRight: ']', Qt.Key_Backslash: '\\',
        Qt.Key_Semicolon: ';', Qt.Key_Apostrophe: "'", Qt.Key_QuoteDbl: '"', 
        Qt.Key_Comma: ',', Qt.Key_Period: '.', Qt.Key_Slash: '/',
        Qt.Key_Agrave: '`',

        # Numpad Keys
        Qt.Key_multiply: 'Num*', Qt.Key_division: 'Num/',
        #Qt.Key_plus: 'Num+', Qt.Key_minus: 'Num-', #not recognized by Qt for some reason
        #Qt.Key_period: 'Num.', #not recognized by Qt for some reason

        # Multimedia keys
        Qt.Key_VolumeUp: 'VolumeUp',
        Qt.Key_VolumeDown: 'VolumeDown',
        Qt.Key_VolumeMute: 'VolumeMute',
        Qt.Key_MediaPlay: 'MediaPlay',
        Qt.Key_MediaStop: 'MediaStop',
        Qt.Key_MediaPrevious: 'MediaPrevious',
        Qt.Key_MediaNext: 'MediaNext',

        # Special Purpose
        Qt.Key_Print: 'PrintScreen',
        Qt.Key_Pause: 'Pause',
        Qt.Key_SysReq: 'SysReq',
        Qt.Key_Help: 'Help',
        Qt.Key_Menu: 'Menu',
    }
    key_list = sorted(list(set(_QT_KEY_TO_STRING_MAP.values())))
    KEY_NAMES_AVAILABLE = ['None'] + key_list


_initialized = False

def ensure_initialized():
    global _initialized
    if not _initialized:
        init()
        _initialized = True
