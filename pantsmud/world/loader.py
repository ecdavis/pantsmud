from pantsmud import storage
from pantsmud.world import link, room, world, zone


def load_links(links_directory_path):
    return storage.load_files(links_directory_path, "*.link.json", link.Link)


def load_rooms(rooms_directory_path):
    return storage.load_files(rooms_directory_path, "*.room.json", room.Room)


def load_world(path):
    return storage.load_file(path, world.World)


def load_zones(zones_directory_path):
    return storage.load_files(zones_directory_path, "*.zone.json", zone.Zone)
