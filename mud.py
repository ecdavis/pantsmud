import logging
import os.path

import pants

from pantsmud import game, hook, net
from pantsmud.world import loader, player

import lib
from lib import login

if __debug__:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

WORLD_PATH = os.path.abspath("data/world/world.json")
ZONE_PATH = os.path.join(os.path.dirname(WORLD_PATH), "zones")
ROOM_PATH = os.path.join(os.path.dirname(WORLD_PATH), "rooms")
LINK_PATH = os.path.join(os.path.dirname(WORLD_PATH), "links")

world = None


def load_world():
    w = loader.load_world(WORLD_PATH)
    for z in loader.load_zones(ZONE_PATH):
        w.add_zone(z)
    for r in loader.load_rooms(ROOM_PATH):
        w.add_room(r)
    for l in loader.load_links(LINK_PATH):
        w.add_link(l)
    return w


def open_brain_hook(_, brain):
    world.add_brain(brain)
    if brain.is_user:
        brain.push_input_handler(login.input_handler, "login")
    else:
        p = player.Player()
        p.brain = brain
        brain.player = p
        world.add_player(p)


def close_brain_hook(_, brain):
    if brain.player:
        brain.player.brain = None
        world.remove_player(brain.player)
    world.remove_brain(brain)

engine = pants.Engine.instance()

world = load_world()
game.init(engine, world)
lib.init()
hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)

server = pants.Server(net.LineStream)
server.listen(4040)
engine.start()
