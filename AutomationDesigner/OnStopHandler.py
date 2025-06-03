# AutomationDesigner/OnStopHandler.py


def onStopHandler(self, NODE_DEFAULT_COLOR, BackdropNode):
    active_loops_were_present = False
    if hasattr(self, '_loop_stop_flags') and self._loop_stop_flags:
        active_loops_were_present = True

        all_start_ids_to_stop = list(self._loop_stop_flags.keys())
        
        for start_id in all_start_ids_to_stop:
            if start_id in self._loop_stop_flags:
                self._loop_stop_flags[start_id].set()
            
            if hasattr(self, '_loop_pause_flags') and start_id in self._loop_pause_flags:
                self._loop_pause_flags[start_id].clear()

            if hasattr(self, '_clear_highlights_for_path'):
                self._clear_highlights_for_path(start_id) 
        
        if hasattr(self, '_active_paths_highlights'):
            self._active_paths_highlights.clear()

    if active_loops_were_present:
        print("[Main] All loops signaled to stop and their highlights cleared.")
    else:
        print("[Main] Stop called, but no active loops were registered to stop.")
