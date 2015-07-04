import uuid

from pantsmud import auxiliary


class Link(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.world = None
        self.node_uuid = None
        self.dest_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_LINK)

    def load_data(self, data):
        # TODO Validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.node_uuid = uuid.UUID(data["node"])
        self.dest_uuid = uuid.UUID(data["dest"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def node(self):
        if self.node_uuid:
            return self.world.nodes[self.node_uuid]
        else:
            return self.node_uuid

    @node.setter
    def node(self, val):
        if val:
            self.node_uuid = val.uuid
        else:
            self.node_uuid = None

    @property
    def dest(self):
        if self.dest_uuid:
            return self.world.nodes[self.dest_uuid]
        else:
            return self.node_uuid

    @dest.setter
    def dest(self, val):
        if val:
            self.dest_uuid = val.uuid
        else:
            self.dest_uuid = None
