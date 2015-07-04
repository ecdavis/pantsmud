from pantsmud import storage
from pantsmud.world import link, node, world, zone


def load_links(links_directory_path):
    return storage.load_files(links_directory_path, "*.link.json", link.Link)


def load_nodes(nodes_directory_path):
    return storage.load_files(nodes_directory_path, "*.node.json", node.Node)


def load_world(path):
    return storage.load_file(path, world.World)


def load_zones(zones_directory_path):
    return storage.load_files(zones_directory_path, "*.zone.json", zone.Zone)
