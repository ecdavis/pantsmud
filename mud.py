import logging
import os.path

import pants

from pantsmud import game, net
from pantsmud.world import link, room, world, zone

import basic_commands, look_commands

if __debug__:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WORLD_PATH = os.path.abspath("data/world/world.json")
ZONE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "zones")
ROOM_PATH = os.path.join(os.path.dirname(WORLD_PATH), "rooms")
LINK_PATH = os.path.join(os.path.dirname(WORLD_PATH), "links")

w = world.load_world(WORLD_PATH)
for z in zone.load_zones(ZONE_PATH):
    w.add_zone(z)
for r in room.load_rooms(ROOM_PATH):
    w.add_room(r)
for l in link.load_links(LINK_PATH):
    w.add_link(l)

engine = pants.Engine.instance()

game.init(engine, w)
basic_commands.init()
look_commands.init()

server = pants.Server(net.LineStream)
server.listen(4040)
engine.start()
