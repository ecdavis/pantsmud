import uuid

from pantsmud.driver import hook, auxiliary


class Zone(object):
    """
    A collection of Nodes into a coherent region of the game world.

    Instances of this class could represent areas in a traditional MUD world, regions of space in an EVE-like game or
    multi-level sections of a dungeon in a roguelike.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""  # TODO this is currently used to build the file path, but it's read from the file data
        self.world = None
        self._reset_interval = -1
        self.reset_timer = -1
        self.node_uuids = set()
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_ZONE)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Zone data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<string>",
                "reset_interval": <int>,
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        # TODO validate loaded data
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.reset_interval = data["reset_interval"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Zone data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "reset_interval": self.reset_interval,
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def nodes(self):
        """
        Get the list of Nodes contained by the Zone.
        """
        return [self.world.nodes[u] for u in self.node_uuids]

    def add_node(self, node):
        """
        Add a Node to the Zone.
        """
        node.zone = self
        self.node_uuids.add(node.uuid)

    @property
    def reset_interval(self):
        """
        Get the Zone's reset interval in minutes.

        A negative interval indicates that the Zone will never be reset.
        """
        return self._reset_interval

    @reset_interval.setter
    def reset_interval(self, interval):
        """
        Set the Zone's reset interval in minutes.

        If the Zone was previously set to never reset, it will now begin to reset as expected. If the current reset
        timer is greater than the new interval, it will be set to the new interval.
        """
        if self.reset_interval < 0 or self.reset_timer > interval:
            self.reset_timer = interval
        self._reset_interval = interval

    def pulse(self):
        """
        Pulse the Zone, i.e. decrement its reset timer.

        When the reset timer reaches zero, the Zone will be reset and the reset timer will be set back to the reset
        interval value.
        """
        self.reset_timer -= 1
        if self.reset_timer == 0:  #
            self.reset_timer = self.reset_interval
            hook.run(hook.HOOK_RESET_ZONE, self)

    def force_reset(self):
        """
        Force the Zone to reset, regardless of the current reset timer value.
        """
        self.reset_timer = 1
        self.pulse()
