from pantsmud import game, hook
from pantsmud.world import player

from lib import login


def open_brain_hook(_, brain):
    game.world.add_brain(brain)
    if brain.is_user:
        brain.push_input_handler(login.input_handler, "login")
    else:
        p = player.Player()
        p.brain = brain
        brain.player = p
        game.world.add_player(p)


def close_brain_hook(_, brain):
    if brain.player:
        brain.player.brain = None
        game.world.remove_player(brain.player)
    game.world.remove_brain(brain)


def init():
    hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
    hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)
