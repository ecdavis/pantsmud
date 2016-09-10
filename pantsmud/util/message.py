import logging

log = logging.getLogger(__name__)


def command_success(actor, cmd, result=None):
    log.debug("command_success")
    actor.message("command.success", {"command": cmd, "result": result})


def command_fail(actor, cmd, args, message):
    log.debug("command_fail")
    actor.message("command.fail", {"command": cmd, "parameters": args, "failure": message})


def command_error(actor, cmd, args, message):
    log.debug("command_error")
    actor.message("command.error", {"command": cmd, "parameters": args, "error": message})


def command_not_found(actor, cmd, args):
    log.debug("command_not_found")
    actor.message("command.not_found", {"command": cmd, "parameters": args})


def command_invalid_input(actor, line):
    log.debug("command_invalid_input")
    actor.message("command.invalid_input", {"input": line})


def command_internal_error(actor):
    log.debug("command_internal_error")
    actor.message("command.internal_error")


def notify(actor, notification, data):
    log.debug("notify")
    actor.message("notify", {"notification": notification, "data": data})
