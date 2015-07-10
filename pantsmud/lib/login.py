import logging

from pantsmud.driver import command, game, message
from pantsmud.world import mobile
from pantsmud.lib import basic_commands

log = logging.getLogger(__name__)

_login_command_manager = command.CommandManager(__name__)


def login_command(brain, cmd, args):
    if not brain.is_user:
        log.error("Brain '%s' tried to execute login_command but it is not a user.", str(brain.uuid))
        message.command_fail(brain, cmd, args)
        return
    if brain.mobile:
        log.error("Brain '%s' tried to execute login_command but it already has a player '%s'.",
                  str(brain.uuid), str(brain.mobile.uuid))
        message.command_fail(brain, cmd, args)
        return
    log.debug("login with args: '%s'", args)  # TODO actually log in
    brain.pop_input_handler()
    brain.push_input_handler(command.input_handler, "playing")
    p = mobile.Mobile()
    p.brain = brain
    brain.mobile = p
    game.world.add_mobile(p)
    brain.message("login.success")


def input_handler(brain, line):
    return _login_command_manager.input_handler(brain, line)


def init():
    _login_command_manager.add("login", login_command)
    _login_command_manager.add("quit", basic_commands.quit_command)
