import logging

from pantsmud import command, hook
from pantsmud.world import player


_engine = None
_world = None
log = logging.getLogger(__name__)


def handle_input(brain, line):
    if brain.input_handlers:
        brain.input_handler(brain, line)
    else:
        log.warning("Received input from brain '%s' but it has no input handlers attached.", brain.uuid)


def pulse_world():
    log.info("Pulsing world...")


def reset_zone_hook(_, zone):
    log.info("Resetting zone: '%s'", zone.name)


def open_brain_hook(_, brain):
    _world.add_brain(brain)
    p = player.Player()
    p.brain = brain
    brain.player = p
    _world.add_player(p)
    brain.push_input_handler(command.input_handler, "playing")


def close_brain_hook(_, brain):
    if brain.player:
        brain.player.brain = None
        _world.remove_player(brain.player)
    _world.remove_brain(brain)


def shutdown_hook(_):
    global _engine, _world
    _engine.stop()
    _engine = None
    _world = None


def init(engine, world):
    global _engine, _world
    _engine = engine
    _world = world
    hook.add(hook.HOOK_RESET_ZONE, reset_zone_hook)
    hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
    hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)
    hook.add(hook.HOOK_SHUTDOWN, shutdown_hook)
    _engine.cycle(60.0, pulse_world)
