# AutomationDesigner/CheckHardStartHandler.py

import shared.globals as g

def checkHardStartHandler(self):
    if g.hard_start:
        print("[Main] Hard start detected! Starting automation.")
        self._on_play()
        g.hard_start = False
    if g.hard_stop:
        print("[Main] Hard stop detected! Stopping automation.")
        self._on_stop()
        g.hard_stop = False