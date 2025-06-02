# nodes/StartNode.py

from NodeGraphQt import (
    BaseNode,
)

class StartNode(BaseNode):
    """
    “Start” node: no properties.
    Fires the loop when PLAY is pressed.
    """
    __identifier__ = 'Automation'
    NODE_NAME = 'Start'

    def __init__(self):
        super(StartNode, self).__init__()
        self.add_output('out')

    def process(self, **kwargs):
        """
        In a real engine, this would “emit” the start‐signal.
        Here it’s stubbed just to show the ID.
        """
        print(f"[StartNode: {self.id}] Fired.")

    def copy(self):
        new_node = StartNode()
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