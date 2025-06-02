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
        new_node = EndNode()
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