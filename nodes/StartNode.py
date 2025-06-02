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