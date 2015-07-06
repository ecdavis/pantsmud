import uuid

from pantsmud import auxiliary, error


class World(object):
    """
    A collection of all the objects in the game world.

    The primary role of this class is to maintain a mapping of object UUIDs to object references. It is also
    responsible for maintaining a valid world state at all times.
    """
    def __init__(self):
        self.sessions = set()
        self.start_node_uuid = None
        self.brains = {}
        self.mobiles = {}
        self.zones = {}
        self.nodes = {}
        self.links = {}
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_WORLD)

    def load_data(self, data):
        """
        Loads a dictionary containing saved World data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "start_node": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.start_node_uuid = uuid.UUID(data["start_node"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing World data ready to be serialized.
        """
        return {
            "start_node": str(self.start_node_uuid),
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def start_node(self):
        """
        Get the starting Node for the World.
        """
        if self.start_node_uuid:
            return self.nodes[self.start_node_uuid]
        else:
            return self.start_node_uuid

    @start_node.setter
    def start_node(self, node):
        """
        Set the starting Node for the world.
        """
        if node:
            self.start_node_uuid = node.uuid
        else:
            self.start_node_uuid = None

    def add_brain(self, brain):
        """
        Add a Brain to the World.
        """
        brain.world = self
        self.brains[brain.uuid] = brain

    def remove_brain(self, brain):
        """
        Remove a Brain from the World.
        """
        del self.brains[brain.uuid]
        brain.world = None

    def add_mobile(self, mobile):
        """
        Add a Mobile to the World.
        """
        mobile.world = self
        self.mobiles[mobile.uuid] = mobile
        self.start_node.add_mobile(mobile)  # TODO improve the whole start_node business

    def remove_mobile(self, mobile):
        """
        Remove a Mobile from the World.
        """
        mobile.node.remove_mobile(mobile)  # TODO improve
        del self.mobiles[mobile.uuid]
        mobile.world = None

    def add_zone(self, zone):
        """
        Add a Zone to the World.
        """
        zone.world = self
        self.zones[zone.uuid] = zone

    def add_node(self, node):
        """
        Add a Node to the World.
        """
        if node.zone_uuid not in self.zones:
            raise error.ZoneNotFound(
                "Node '%s' has zone_uuid '%s' that was not found on the World '%r'." % (str(node.uuid),
                                                                                        str(node.zone_uuid),
                                                                                        self)
            )
        node.world = self
        node.zone.add_node(node)
        self.nodes[node.uuid] = node

    def add_link(self, link):
        """
        Add a Link to the World.
        """
        if link.node_uuid not in self.nodes:
            raise error.NodeNotFound(
                "Link '%s' has node_uuid '%s' that was not found on the World '%r'." % (str(link.uuid),
                                                                                        str(link.node_uuid),
                                                                                        self)
            )
        if link.dest_uuid not in self.nodes:
            raise error.NodeNotFound(
                "Link '%s' has dest_uuid '%s' that was not found on the World '%r'." % (str(link.uuid),
                                                                                        str(link.dest_uuid),
                                                                                        self)
            )
        link.world = self
        link.node.add_link(link)
        self.links[link.uuid] = link

    def pulse(self):
        """
        Pulse all Zones contained by the World.
        """
        for key, zone in self.zones.iteritems():
            zone.pulse()

    def force_reset(self):
        """
        Force all Zones contained by the World to reset.
        """
        for key, zone in self.zones.iteritems():
            zone.force_reset()
