import uuid

from pantsmud import auxiliary


class Link(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.world = None
        self.room_uuid = None
        self.dest_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_LINK)

    def load_data(self, data):
        # TODO Validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.room_uuid = uuid.UUID(data["room"])
        self.dest_uuid = uuid.UUID(data["dest"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def room(self):
        if self.room_uuid:
            return self.world.rooms[self.room_uuid]
        else:
            return self.room_uuid

    @room.setter
    def room(self, val):
        if val:
            self.room_uuid = val.uuid
        else:
            self.room_uuid = None

    @property
    def dest(self):
        if self.dest_uuid:
            return self.world.rooms[self.dest_uuid]
        else:
            return self.room_uuid

    @dest.setter
    def dest(self, val):
        if val:
            self.dest_uuid = val.uuid
        else:
            self.dest_uuid = None
