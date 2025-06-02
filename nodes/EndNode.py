# nodes/EndNode.py

from NodeGraphQt import (
    BaseNode,
)

class EndNode(BaseNode):
    """
    “End” node: no properties.
    When a loop reaches this node, it will return to its Start node.
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'End'

    def __init__(self):
        super(EndNode, self).__init__()
        # Only an input socket (since “End” receives a signal)
        self.add_input('in')

        #self.add_checkbox('loopable', 'Hard Stop', False)
        self.add_combo_menu('repeat', 'Repeat', ['Single', 'Repeat'])
        self.set_property('repeat', 'Repeat')

    def process(self, **kwargs):
        """
        In a real engine, this would mark the loop’s end.
        Here it’s stubbed just to show the ID.
        """
        print(f"[EndNode: {self.id}] Reached. Repeat: {self.get_property('repeat')}")

        
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
            print(f"  [EndNode.copy] ERROR during collection from self.properties(): {e}")

        custom_widget_prop_names = ['repeat']
        for name in custom_widget_prop_names:
            try:
                val = self.get_property(name) 
                props[name] = val
            except Exception as e:
                print(f"    [EndNode.copy] ERROR collecting explicitly for '{name}': {e}. It will not be copied.")
                
        return (self.id, self.__class__, props, (orig_x, orig_y))