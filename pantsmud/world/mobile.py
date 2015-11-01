import uuid

from pantsmud.driver import auxiliary


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

    def load_data(self, data):
        """
        Loads a dictionary containing saved Mobile data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        # TODO validate loaded data
        self.uuid = uuid.UUID(data["uuid"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Mobile data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def brain(self):
        """
        Get the Mobile's Brain, if it has one.
        """
        if self.brain_uuid:
            return self.world.brains[self.brain_uuid]
        else:
            return self.brain_uuid

    @brain.setter
    def brain(self, brain):
        """
        Set the Mobile's Brain.
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

    def attach_brain(self, brain):
        """
        Attach a Brain to this Mobile.
        """
        self.brain = brain
        brain.mobile = self

    def detach_brain(self):
        """
        Detach a Brain from this Mobile.
        """
        self.brain.mobile = None
        self.brain = None

    def message(self, name, data=None):
        """
        Send a message to the Mobile's Brain, if it has one.
        """
        if self.brain:
            self.brain.message(name, data)
