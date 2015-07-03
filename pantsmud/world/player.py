import uuid

from pantsmud import auxiliary


class Player(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.world = None
        self.brain_uuid = None
        self.room_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_PLAYER)

    @property
    def brain(self):
        if self.brain_uuid is None:
            return None
        else:
            return self.world.brains[self.brain_uuid]

    @brain.setter
    def brain(self, val):
        if val is None:
            self.brain_uuid = None
        else:
            self.brain_uuid = val.uuid

    @property
    def room(self):
        if self.room_uuid is None:
            return None
        else:
            return self.world.rooms[self.room_uuid]

    @room.setter
    def room(self, val):
        if val is None:
            self.room_uuid = None
        else:
            self.room_uuid = val.uuid

