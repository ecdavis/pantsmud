"""
A pub/sub implementation that allows developers to extend the game without having to modify the driver code.

A hook is a mapping of a string to a list of functions. When a hook is run, each function in its list is executed.
Hooks can be added using the add function and run using the run function. When writing discrete modules for PantsMUD,
adding your own hooks is strongly encouraged.
"""

import logging

log = logging.getLogger(__name__)


HOOK_CLOSE_BRAIN = "close_brain"
HOOK_OPEN_BRAIN = "open_brain"
HOOK_RESET_ZONE = "reset_zone"
HOOK_SHUTDOWN = "shutdown"


# name: [func]
_hooks = {}


def add(hook, func):
    """
    Add a function to the given hook.
    """
    if not callable(func):
        raise TypeError("'func' must be callable.")
    if hook not in _hooks:
        log.debug("Adding new hook: '%s'", hook)
        _hooks[hook] = []
    assert func not in _hooks[hook]
    log.debug("Adding new hook function: '%s', hook '%s'", func.__name__, hook)
    _hooks[hook].append(func)


def run(hook, *args, **kwargs):
    """
    Run the given hook, passing the args and kwargs through to all the hook functions.
    """
    if hook not in _hooks:
        log.debug("Tried to run non-existent hook: '%s'", hook)
        return
    for func in _hooks[hook]:
        try:
            func(hook, *args, **kwargs)
        except Exception:  # Catch Exception here because we have no control over what hook code will throw.
            log.exception("Unhandled exception in hook function: '%s', hook '%s'", func.__name__, hook)


def init():
    global _hooks
    _hooks = {}
