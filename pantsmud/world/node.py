import uuid

from pantsmud import auxiliary


class Node(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.world = None
        self.zone_uuid = None
        self.link_table = {}  # name: uuid
        self.mobile_uuids = set()
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_NODE)

    def load_data(self, data):
        # TODO validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.zone_uuid = uuid.UUID(data["zone"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def zone(self):
        if self.zone_uuid:
            return self.world.zones[self.zone_uuid]
        else:
            return self.zone_uuid

    @zone.setter
    def zone(self, val):
        if val:
            self.zone_uuid = val.uuid
        else:
            self.zone_uuid = None

    @property
    def mobiles(self):
        return set([self.world.mobiles[u] for u in self.mobile_uuids])

    def add_mobile(self, mobile):
        mobile.node = self
        self.mobile_uuids.add(mobile.uuid)

    def remove_mobile(self, mobile):
        self.mobile_uuids.remove(mobile.uuid)
        mobile.node = None

    @property
    def links(self):
        return [self.world.links[u] for u in self.link_table.itervalues()]

    def get_link(self, name):
        if name not in self.link_table:
            raise Exception("TODO")  # TODO
        return self.world.links[self.link_table[name]]

    def add_link(self, link):
        if link.name in self.link_table:
            raise Exception("TODO")  # TODO
        link.node = self
        self.link_table[link.name] = link.uuid
