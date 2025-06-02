# handlers/KeyboardListener.py

import shared.globals as g

from pynput.keyboard import (
    Key,
    Listener as KeyboardListener,
)


def on_press(key):
    try:
        if key == Key.f1:
            print("F1 key pressed!")
        if key == Key.f2:
            print("F2 key pressed!")
        elif key == Key.f3:
            g.show_coords = not g.show_coords
    except AttributeError:
        pass

def on_release(key):
    if key == Key.f1:
        g.hard_start = True
    if key == Key.f2:
        g.hard_stop = True

    
keyboardListener = KeyboardListener(on_press=on_press, on_release=on_release)