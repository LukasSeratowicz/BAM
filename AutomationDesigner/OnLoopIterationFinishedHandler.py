# AutomationDesigner/OnLoopIterationFinishedHandler.py

from PySide6.QtCore import QTimer

def onLoopIterationFinishedHandler(self, start_id: str):
        print(f"[Main] Loop iteration finished for Start Node {start_id}.")
        if start_id in self._loop_stop_flags and self._loop_stop_flags[start_id].is_set():
                QTimer.singleShot(0, lambda: self._clear_highlights_for_path(start_id))
                if start_id in self._loop_threads: del self._loop_threads[start_id]
                if start_id in self._loop_stop_flags: del self._loop_stop_flags[start_id]
                if start_id in self._loop_pause_flags: del self._loop_pause_flags[start_id]