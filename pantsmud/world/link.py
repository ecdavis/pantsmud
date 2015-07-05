import uuid

from pantsmud import auxiliary


class Link(object):
    """
    A means of moving from one Node to another.

    Instances of this class could represent directional exits in a traditional MUD, jump gates in an EVE-like game or
    inter-level staircases in a roguelike.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""  # TODO remove
        self.world = None
        self.node_uuid = None
        self.dest_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_LINK)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Link data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<string>",
                "node": "<uuid>",
                "dest": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        # TODO Validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.node_uuid = uuid.UUID(data["node"])
        self.dest_uuid = uuid.UUID(data["dest"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def node(self):
        """
        Get the container Node for this Link.
        """
        if self.node_uuid:
            return self.world.nodes[self.node_uuid]
        else:
            return self.node_uuid

    @node.setter
    def node(self, node):
        """
        Set the container Node for this Link.
        """
        if node:
            self.node_uuid = node.uuid
        else:
            self.node_uuid = None

    @property
    def dest(self):
        """
        Get the destination Node for this Link.
        """
        if self.dest_uuid:
            return self.world.nodes[self.dest_uuid]
        else:
            return self.node_uuid

    @dest.setter
    def dest(self, node):
        """
        Set the destination Node for this Link.
        """
        if node:
            self.dest_uuid = node.uuid
        else:
            self.dest_uuid = None
