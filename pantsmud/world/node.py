import uuid

from pantsmud import auxiliary


class Node(object):
    """
    A representation of a discrete location in the game world.

    Instances of this class could represent rooms in a traditional MUD world, solar systems in an EVE-like game or
    dungeon levels in a roguelike.

    A general rule of thumb to follow is that game entities (i.e. mobiles, items, etc.) can only modify the state of
    their current Node.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.world = None
        self.zone_uuid = None
        self.link_table = {}  # name: uuid
        self.mobile_uuids = set()
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_NODE)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Node data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<string>",
                "zone": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        # TODO validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.zone_uuid = uuid.UUID(data["zone"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def zone(self):
        """
        Get the container Zone for this Node.
        """
        if self.zone_uuid:
            return self.world.zones[self.zone_uuid]
        else:
            return self.zone_uuid

    @zone.setter
    def zone(self, zone):
        """
        Set the container Zone for this Node.
        """
        if zone:
            self.zone_uuid = zone.uuid
        else:
            self.zone_uuid = None

    @property
    def mobiles(self):
        """
        Get the list of Mobiles contained by this Node.
        """
        return [self.world.mobiles[u] for u in self.mobile_uuids]

    def add_mobile(self, mobile):
        """
        Add a Mobile to the Node.
        """
        mobile.node = self
        self.mobile_uuids.add(mobile.uuid)

    def remove_mobile(self, mobile):
        """
        Remove a Mobile from the Node.
        """
        self.mobile_uuids.remove(mobile.uuid)
        mobile.node = None

    @property
    def links(self):
        """
        Get the list of Links contained by this Node.
        """
        return [self.world.links[u] for u in self.link_table.itervalues()]

    # TODO Remove this method or change it to use Link.uuid
    def get_link(self, name):
        """
        Get the Link with the given game if it is contained by this Node.
        """
        if name not in self.link_table:
            raise Exception("TODO")  # TODO
        return self.world.links[self.link_table[name]]

    def add_link(self, link):
        """
        Add a Link to the Node.
        """
        if link.name in self.link_table:
            raise Exception("TODO")  # TODO
        link.node = self
        self.link_table[link.name] = link.uuid