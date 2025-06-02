# AutomationDesigner/OnPauseHandler.py

def onPauseHandler(self):
    for start_id, pause_event in self._loop_pause_flags.items():
        pause_event.set()
    print("[Main] All loops paused. (will resume when Play is clicked again)")