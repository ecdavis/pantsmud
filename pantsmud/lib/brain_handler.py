from pantsmud.driver import game, hook
from pantsmud.world import mobile

from pantsmud.lib import login


def open_brain_hook(_, brain):
    game.world.add_brain(brain)
    if brain.is_user:
        brain.push_input_handler(login.input_handler, "login")
    else:
        p = mobile.Mobile()
        p.brain = brain
        brain.mobile = p
        game.world.add_mobile(p)


def close_brain_hook(_, brain):
    if brain.mobile:
        brain.mobile.brain = None
        game.world.remove_mobile(brain.mobile)
    game.world.remove_brain(brain)


def init():
    hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
    hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)
