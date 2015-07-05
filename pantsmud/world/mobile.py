import uuid

from pantsmud import auxiliary


class Mobile(object):
    """
    A representation of a mobile entity in the game world.

    Instances of this class could represent mobs in a traditional MUD world, ships in an EVE-like game or monsters in a
    roguelike.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.world = None
        self.brain_uuid = None
        self.node_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_MOBILE)

    @property
    def brain(self):
        """
        Get the Brain attached to this Mobile.
        """
        if self.brain_uuid:
            return self.world.brains[self.brain_uuid]
        else:
            return self.brain_uuid

    @brain.setter
    def brain(self, brain):
        """
        Attach a Brain to this Mobile.
        """
        if brain:
            self.brain_uuid = brain.uuid
        else:
            self.brain_uuid = None

    @property
    def node(self):
        """
        Get the container Node for this Mobile.
        """
        if self.node_uuid:
            return self.world.nodes[self.node_uuid]
        else:
            return self.node_uuid

    @node.setter
    def node(self, node):
        """
        Set the container Node for this Mobile.
        """
        if node:
            self.node_uuid = node.uuid
        else:
            self.node_uuid = None
