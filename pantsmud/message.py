import logging

log = logging.getLogger(__name__)


def command_notfound(brain, cmd, args):
    log.debug("command_notfound")
    brain.message("command.notfound", {"command": cmd, "parameters": args})

def command_fail(brain, cmd, args):
    log.debug("command_fail")
    brain.message("command.fail", {"command": cmd, "parameters": args})
