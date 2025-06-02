# nodes/DelayNode.py

from NodeGraphQt import (
    BaseNode,
)
import time

class DelayNode(BaseNode):
    """
    “Delay” node: pauses execution for a given number of milliseconds.
      • delay: Text input (ms to pause)
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Delay'

    def __init__(self):
        super(DelayNode, self).__init__()
        # One input and one output socket
        self.add_input('in')
        self.add_output('out')

        # Numeric field as text input
        self.add_text_input('delay', 'Delay (ms)')
        self.set_property('delay', '1000')

    def process(self, stop_event=None, **kwargs):
        """
        Sleep for the specified number of milliseconds, in 100ms chunks,
        printing status each chunk so you see the delay happening.
        """
        try:
            ms_total = int(self.get_property('delay'))
        except ValueError:
            ms_total = 0

        print(f"[DelayNode: {self.id}] Beginning {ms_total} ms delay.")
        # Break into 100ms increments so we can see progress
        ms_done = 0
        while ms_done < ms_total:
            
            if stop_event and stop_event.is_set():
                print(f"[DelayNode: {self.id}] Stopped early at {ms_done}/{ms_total} ms")
                return
            
            chunk = min(100, ms_total - ms_done)
            time.sleep(chunk / 1000.0)
            ms_done += chunk
            #print(f"[DelayNode: {self.id}] still sleeping... {ms_done}/{ms_total} ms")
        print(f"[DelayNode: {self.id}] Completed delay.")

        
    def copy(self):
        new_node = DelayNode()
        for prop_name, _ in self.properties().items():
            if prop_name in ('inputs', 'outputs', 'id'):
                continue
            try:
                new_node.set_property(prop_name, self.get_property(prop_name))
            except Exception:
                pass

        pos = self.pos()
        try:
            x, y = pos.x(), pos.y()
        except AttributeError:
            x, y = pos[0], pos[1]
        new_node.set_pos(x + 20, y + 20)

        return new_node