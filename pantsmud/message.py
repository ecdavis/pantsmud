import logging

log = logging.getLogger(__name__)


def command_not_found(brain, cmd, args):
    log.debug("command_not_found")
    brain.message("command.not_found", {"command": cmd, "parameters": args})


def command_fail(brain, cmd, args):
    log.debug("command_fail")
    brain.message("command.fail", {"command": cmd, "parameters": args})


def command_invalid_input(brain, line):
    log.debug("command_invalid_input")
    brain.message("command.invalid_input", {"input": line})
