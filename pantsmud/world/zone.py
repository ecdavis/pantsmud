import uuid

from pantsmud import auxiliary, hook


class Zone(object):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.world = None
        self._reset_interval = -1
        self.reset_timer = -1
        self.room_uuids = set()
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_ZONE)

    def load_data(self, data):
        # TODO validation
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.reset_interval = data["reset_interval"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    @property
    def rooms(self):
        return [self.world.rooms[u] for u in self.room_uuids]

    @property
    def reset_interval(self):
        return self._reset_interval

    @reset_interval.setter
    def reset_interval(self, val):
        if self.reset_interval < 0 or self.reset_timer > val:
            self.reset_timer = val
        self._reset_interval = val

    def add_room(self, room):
        room.zone = self
        self.room_uuids.add(room.uuid)

    def pulse(self):
        self.reset_timer -= 1
        if self.reset_timer == 0:  #
            self.reset_timer = self.reset_interval
            hook.run(hook.HOOK_RESET_ZONE, self)

    def force_reset(self):
        self.reset_timer = 1
        self.pulse()
