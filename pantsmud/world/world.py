from pantsmud import auxiliary


class World(object):
    def __init__(self):
        self.sessions = set()
        self.start_node = None
        self.brains = {}
        self.mobiles = {}
        self.zones = {}
        self.nodes = {}
        self.links = {}
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_WORLD)

    def load_data(self, data):
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def add_brain(self, brain):
        brain.world = self
        self.brains[brain.uuid] = brain

    def remove_brain(self, brain):
        del self.brains[brain.uuid]
        brain.world = None

    def add_mobile(self, mobile):
        mobile.world = self
        self.mobiles[mobile.uuid] = mobile
        self.start_node.add_mobile(mobile)  # TODO

    def remove_mobile(self, mobile):
        mobile.node.remove_mobile(mobile)  # TODO
        del self.mobiles[mobile.uuid]
        mobile.world = None

    def add_zone(self, zone):
        zone.world = self
        self.zones[zone.uuid] = zone

    def add_node(self, node):
        if node.zone_uuid not in self.zones:
            raise Exception("TODO")  # TODO
        node.world = self
        node.zone.add_node(node)
        if len(self.nodes) < 1:  # TODO
            self.start_node = node
        self.nodes[node.uuid] = node

    def add_link(self, link):
        if link.node_uuid not in self.nodes:
            raise Exception("TODO")  # TODO
        if link.dest_uuid not in self.nodes:
            raise Exception("TODO")  # TODO
        link.world = self
        link.node.add_link(link)
        self.links[link.uuid] = link

    def pulse(self):
        for key, zone in self.zones.iteritems():
            zone.pulse()

    def force_reset(self):
        for key, zone in self.zones.iteritems():
            zone.force_reset()
