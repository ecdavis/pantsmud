import logging

log = logging.getLogger(__name__)


engine = None
environment = None


def pulse():
    environment.pulse()


def shutdown_hook():
    global engine, environment
    engine.stop()
    engine = None
    environment = None


def init(eng, env):
    global engine, environment
    engine = eng
    environment = env


def start():
    engine.cycle(60.0, pulse)
    engine.start()


def handle_input(brain, line):
    if not line:
        log.debug("Ignoring empty input from brain '%s'.", brain.uuid)
        return
    if brain.input_handlers:
        brain.input_handler(brain, line)
    else:
        log.error("Received input from brain '%s' but it has no input handlers attached.", brain.uuid)
