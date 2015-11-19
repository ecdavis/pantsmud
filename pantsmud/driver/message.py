import logging

log = logging.getLogger(__name__)


def command_error(brain, cmd, args, message):
    log.debug("command_error")
    brain.message("command.error", {"command": cmd, "parameters": args, "error": message})


def command_not_found(brain, cmd, args):
    log.debug("command_not_found")
    brain.message("command.not_found", {"command": cmd, "parameters": args})


def command_fail(brain, cmd, args):
    log.debug("command_fail")
    brain.message("command.fail", {"command": cmd, "parameters": args})


def command_invalid_input(brain, line):
    log.debug("command_invalid_input")
    brain.message("command.invalid_input", {"input": line})


def command_internal_error(brain):
    log.debug("command_internal_error")
    brain.message("command.internal_error")
