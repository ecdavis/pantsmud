import uuid

from pantsmud import auxiliary, storage


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
        return self.world.rooms[self.room_uuid]

    @room.setter
    def room(self, val):
        self.room_uuid = val.uuid

    @property
    def dest(self):
        return self.world.rooms[self.dest_uuid]

    @dest.setter
    def dest(self, val):
        self.dest_uuid = val.uuid


def load_links(links_directory_path):
    return storage.load_files(links_directory_path, "*.link.json", Link)
