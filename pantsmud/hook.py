import logging

log = logging.getLogger(__name__)


HOOK_CLOSE_BRAIN = "close_brain"
HOOK_OPEN_BRAIN = "open_brain"
HOOK_RESET_ZONE = "reset_zone"
HOOK_SHUTDOWN = "shutdown"


# name: [func]
_hooks = {}


def add(name, func):
    if name not in _hooks:
        log.debug("Adding new hook type: '%s'", name)
        _hooks[name] = []
    log.debug("Adding new hook: '%s', type '%s'", func.__name__, name)
    _hooks[name].append(func)


def run(name, *args, **kwargs):
    if name not in _hooks:
        return
    for func in _hooks[name]:
        try:
            func(name, *args, **kwargs)
        except Exception:
            log.exception("Unhandled exception in hook: '%s', func '%s'", name, func.__name__)
