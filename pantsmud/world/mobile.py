import uuid

from pantsmud import auxiliary


class Mobile(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.world = None
        self.brain_uuid = None
        self.node_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_MOBILE)

    @property
    def brain(self):
        if self.brain_uuid:
            return self.world.brains[self.brain_uuid]
        else:
            return self.brain_uuid

    @brain.setter
    def brain(self, val):
        if val:
            self.brain_uuid = val.uuid
        else:
            self.brain_uuid = None

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
