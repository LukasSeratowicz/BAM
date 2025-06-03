# nodes/StartNode.py

import shared.globals as g

from NodeGraphQt import (
    BaseNode,
)

class StartNode(BaseNode):
    """
    “Start” node: `key` - start key to trigger the loop.
    Fires the loop when PLAY is pressed.
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Start'

    def __init__(self):
        super(StartNode, self).__init__()
        self.add_output('out')

        
        self.add_combo_menu('key', 'Key', g.KEY_NAMES_AVAILABLE)
        self.set_property('key', 'None')
        

    def process(self, **kwargs):
        """
        In a real engine, this would “emit” the start‐signal.
        Here it’s stubbed just to show the ID.
        """
        print(f"[StartNode: {self.id}] Fired (Key: {self.get_property('key')}).")

    def copy(self):
        node_pos = self.pos() 
        try:
            orig_x, orig_y = node_pos.x(), node_pos.y()
        except AttributeError: 
            orig_x, orig_y = node_pos[0], node_pos[1]

        props = {}

        try:
            all_prop_keys = list(self.properties().keys())
            for name in all_prop_keys:
                if name not in ('inputs', 'outputs', 'id'):
                    val = self.get_property(name)
                    props[name] = val
        except Exception as e:
            print(f"  [StartNode.copy] ERROR during collection from self.properties(): {e}")

        custom_widget_prop_names = ['key']
        for name in custom_widget_prop_names:
            try:
                val = self.get_property(name) 
                props[name] = val
            except Exception as e:
                print(f"    [StartNode.copy] ERROR collecting explicitly for '{name}': {e}. It will not be copied.")

        return (self.id, self.__class__, props, (orig_x, orig_y))