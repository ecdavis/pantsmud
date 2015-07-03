from pantsmud import auxiliary, storage


class World(object):
    def __init__(self):
        self.sessions = set()
        self.start_room = None
        self.brains = {}
        self.players = {}
        self.zones = {}
        self.rooms = {}
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

    def add_player(self, player):
        player.world = self
        self.players[player.uuid] = player
        self.start_room.add_player(player)  # TODO

    def remove_player(self, player):
        player.room.remove_player(player)  # TODO
        del self.players[player.uuid]
        player.world = None

    def add_zone(self, zone):
        zone.world = self
        self.zones[zone.uuid] = zone

    def add_room(self, room):
        if room.zone_uuid not in self.zones:
            raise Exception("TODO")  # TODO
        room.world = self
        room.zone.add_room(room)
        if len(self.rooms) < 1:  # TODO
            self.start_room = room
        self.rooms[room.uuid] = room

    def add_link(self, link):
        if link.room_uuid not in self.rooms:
            raise Exception("TODO")  # TODO
        if link.dest_uuid not in self.rooms:
            raise Exception("TODO")  # TODO
        link.world = self
        link.room.add_link(link)
        self.links[link.uuid] = link

    def pulse(self):
        for key, zone in self.zones.iteritems():
            zone.pulse()

    def force_reset(self):
        for key, zone in self.zones.iteritems():
            zone.force_reset()


def load_world(path):
    return storage.load_file(path, World)
