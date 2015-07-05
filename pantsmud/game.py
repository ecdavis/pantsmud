import logging

from pantsmud import hook


engine = None
world = None
log = logging.getLogger(__name__)


def handle_input(brain, line):
    if not line:
        log.debug("Ignoring empty input from brain '%s'.", brain.uuid)
        return
    if brain.input_handlers:
        brain.input_handler(brain, line)
    else:
        log.error("Received input from brain '%s' but it has no input handlers attached.", brain.uuid)


def pulse_world():
    log.info("Pulsing world...")


def reset_zone_hook(_, zone):
    log.info("Resetting zone: '%s'", zone.name)


def shutdown_hook(_):
    global engine, world
    engine.stop()
    engine = None
    world = None


def init(e, w):
    global engine, world
    engine = e
    world = w
    hook.add(hook.HOOK_RESET_ZONE, reset_zone_hook)
    hook.add(hook.HOOK_SHUTDOWN, shutdown_hook)
    engine.cycle(60.0, pulse_world)
