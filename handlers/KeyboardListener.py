# handlers/KeyboardListener.py

import shared.globals as g

from pynput import keyboard

_PYNPUT_SPECIAL_KEY_TO_STRING_MAP = {
    # Function Keys (F1-F3 are global hotkeys for start/stop/show coords)
    keyboard.Key.f4: 'F4', keyboard.Key.f5: 'F5', keyboard.Key.f6: 'F6',
    keyboard.Key.f7: 'F7', keyboard.Key.f8: 'F8', keyboard.Key.f9: 'F9',
    keyboard.Key.f10: 'F10', keyboard.Key.f11: 'F11', keyboard.Key.f12: 'F12',

    # Standard Action/Navigation Keys
    keyboard.Key.enter: 'Enter',
    keyboard.Key.space: 'Space',
    keyboard.Key.tab: 'Tab',
    keyboard.Key.esc: 'Esc',
    keyboard.Key.backspace: 'Backspace',
    keyboard.Key.delete: 'Delete',
    keyboard.Key.insert: 'Insert',
    keyboard.Key.home: 'Home',
    keyboard.Key.end: 'End',
    keyboard.Key.page_up: 'PageUp',
    keyboard.Key.page_down: 'PageDown',

    # Arrow Keys
    keyboard.Key.up: 'Up', keyboard.Key.down: 'Down',
    keyboard.Key.left: 'Left', keyboard.Key.right: 'Right',

    # Modifier Keys
    keyboard.Key.shift: 'Shift', keyboard.Key.shift_l: 'Shift', keyboard.Key.shift_r: 'Shift',
    keyboard.Key.ctrl: 'Ctrl', keyboard.Key.ctrl_l: 'Ctrl', keyboard.Key.ctrl_r: 'Ctrl',
    keyboard.Key.alt: 'Alt', keyboard.Key.alt_l: 'Alt', keyboard.Key.alt_r: 'Alt',
    # keyboard.Key.alt_gr: 'AltGr',
    keyboard.Key.cmd: 'Meta', keyboard.Key.cmd_l: 'Meta', keyboard.Key.cmd_r: 'Meta', # Windows/Command key

    keyboard.Key.caps_lock: 'CapsLock',
    keyboard.Key.num_lock: 'NumLock',
    keyboard.Key.scroll_lock: 'ScrollLock',

    # Special Purpose
    keyboard.Key.print_screen: 'PrintScreen',
    keyboard.Key.pause: 'Pause',
    keyboard.Key.menu: 'Menu',
    # keyboard.Key.sys_req: 'SysReq',

    # Multimedia keys
    keyboard.Key.media_volume_up: 'VolumeUp',
    keyboard.Key.media_volume_down: 'VolumeDown',
    keyboard.Key.media_volume_mute: 'VolumeMute',
    keyboard.Key.media_play_pause: 'MediaPlay',
    #keyboard.Key.media_stop: 'MediaStop',
    keyboard.Key.media_previous: 'MediaPrevious',
    keyboard.Key.media_next: 'MediaNext',
}

_KEYPAD_KEY_CODES_TO_STRING_MAP = {
    96: 'Num0',  # Numpad 0
    97: 'Num1',  # Numpad 1
    98: 'Num2',  # Numpad 2
    99: 'Num3',  # Numpad 3
    100: 'Num4', # Numpad 4
    101: 'Num5', # Numpad 5
    102: 'Num6', # Numpad 6
    103: 'Num7', # Numpad 7
    104: 'Num8', # Numpad 8
    105: 'Num9', # Numpad 9
    110: 'Num.',# Numpad .
}

def on_press(key):
    if key == keyboard.Key.f1:
        g.hard_start = True
        return
    if key == keyboard.Key.f2:
        g.hard_stop = True
        return
    if key == keyboard.Key.f3:
        g.show_coords = not g.show_coords
        return 


    key_str = None
    try:
        if isinstance(key, keyboard.Key):
            key_str = _PYNPUT_SPECIAL_KEY_TO_STRING_MAP.get(key)
        elif isinstance(key, keyboard.KeyCode):
            if hasattr(key, 'vk') and key.vk in _KEYPAD_KEY_CODES_TO_STRING_MAP:
                key_str = _KEYPAD_KEY_CODES_TO_STRING_MAP[key.vk]
            elif key.char is not None:
                char = key.char
                print(f"Key pressed: {char}")
                key_str = key.char.upper() if len(key.char) == 1 and key.char.isalpha() else key.char
    except AttributeError:
        # Some keys might not have 'char' (e.g. dead keys on some layouts)
        print(f"Error processing key {key}")
        pass

    if key_str and key_str in g.KEY_NAMES_AVAILABLE and key_str != 'None':
        # if key_str not in ['F1', 'F2', 'F3']:
        print(f"Global key pressed: {key_str}")
        g.GLOBAL_KEY_PRESS_STATE[key_str] = True
    else:
        print(f"Key {key} not recognized or not in available keys!")


def on_release(key):
    pass

    
keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)