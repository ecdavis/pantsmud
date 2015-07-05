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


def save_world(path, world):
    """
    Save the World data to the given path.
    """
    return storage.save_object(path, world)


def save_links(path, world):
    """
    Save all Link data to files under the given path.
    """
    return storage.save_objects(path, ".link.json", world.links.values())


def save_nodes(path, world):
    """
    Save all Node data to files under the given path.
    """
    return storage.save_objects(path, ".node.json", world.nodes.values())


def save_zones(path, world):
    """
    Save all Zone data to files under the given path.
    """
    return storage.save_objects(path, ".zone.json", world.zones.values())
