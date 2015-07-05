from pantsmud import storage
from pantsmud.world import link, node, world, zone


def load_world(path):
    """
    Load the World data stored at the given path.
    """
    return storage.load_file(path, world.World)


def load_links(path):
    """
    Load all Link data stored under the given path. This function is not recursive.
    """
    return storage.load_files(path, "*.link.json", link.Link)


def load_nodes(path):
    """
    Load all Node data stored under the given path. This function is not recursive.
    """
    return storage.load_files(path, "*.node.json", node.Node)


def load_zones(path):
    """
    Load all Zone data stored under the given path. This function is not recursive.
    """
    return storage.load_files(path, "*.zone.json", zone.Zone)
