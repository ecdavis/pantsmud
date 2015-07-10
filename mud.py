import logging
import os.path

import pants

from pantsmud.driver import game, net
import pantsmud.lib
from pantsmud.world import persist

if __debug__:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WORLD_PATH = os.path.abspath("data/world/world.json")
ZONE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "zones")
NODE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "nodes")
LINK_PATH = os.path.join(os.path.dirname(WORLD_PATH), "links")


def load_world():
    w = persist.load_world(WORLD_PATH)
    for z in persist.load_zones(ZONE_PATH):
        w.add_zone(z)
    for r in persist.load_nodes(NODE_PATH):
        w.add_node(r)
    for l in persist.load_links(LINK_PATH):
        w.add_link(l)
    return w


def save_world(w):
    persist.save_links(LINK_PATH, w)
    persist.save_nodes(NODE_PATH, w)
    persist.save_zones(ZONE_PATH, w)
    persist.save_world(WORLD_PATH, w)

engine = pants.Engine.instance()
world = load_world()

game.init(engine, world)
pantsmud.lib.init()
net.init()

engine.start()

save_world(world)
