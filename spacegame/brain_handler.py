from pantsmud.driver import game, hook
from pantsmud.world import mobile

from spacegame import login, user


def open_brain_hook(_, brain):
    game.world.add_brain(brain)
    if brain.is_user:
        brain.push_input_handler(login.login_input_handler, "login")
    else:
        # TODO input handler for the brain??
        mob = mobile.Mobile()
        mob.attach_brain(brain)
        game.world.add_mobile(mob)


def close_brain_hook(_, brain):
    mob = brain.mobile
    if brain.is_user:
        user.save_player(mob)
    mob.detach_brain()
    game.world.remove_mobile(mob)
    game.world.remove_brain(brain)


def init():
    hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
    hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)
