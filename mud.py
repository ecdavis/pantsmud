import logging
import os.path

import pants

from pantsmud import game, net
from pantsmud.world import loader

import lib

if __debug__:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WORLD_PATH = os.path.abspath("data/world/world.json")
ZONE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "zones")
ROOM_PATH = os.path.join(os.path.dirname(WORLD_PATH), "rooms")
LINK_PATH = os.path.join(os.path.dirname(WORLD_PATH), "links")


def load_world():
    w = loader.load_world(WORLD_PATH)
    for z in loader.load_zones(ZONE_PATH):
        w.add_zone(z)
    for r in loader.load_rooms(ROOM_PATH):
        w.add_room(r)
    for l in loader.load_links(LINK_PATH):
        w.add_link(l)
    return w

engine = pants.Engine.instance()
world = load_world()

game.init(engine, world)
lib.init()
net.init()

engine.start()
