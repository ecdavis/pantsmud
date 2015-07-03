import logging

log = logging.getLogger(__name__)


def command_fail(brain, cmd, args):
    log.debug("command_fail")
    brain.message("command.fail", {"command": cmd, "parameters": args, "reason": "internal server error"})
