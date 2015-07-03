import logging

from pantsmud import command, game, message
from pantsmud.world import player

import basic_commands

log = logging.getLogger(__name__)

_login_command_manager = command.CommandManager("login")


def login_command(brain, cmd, args):
    if not brain.is_user:
        log.error("Brain '%s' tried to execute login_command but it is not a user.", str(brain.uuid))
        message.command_fail(brain, cmd, args)
        return
    if brain.player:
        log.error("Brain '%s' tried to execute login_command but it already has a player '%s'.",
                  str(brain.uuid), str(brain.player.uuid))
        message.command_fail(brain, cmd, args)
        return
    log.debug("login with args: '%s'", args)  # TODO actually log in
    brain.pop_input_handler()
    brain.push_input_handler(command.input_handler, "playing")
    p = player.Player()
    p.brain = brain
    brain.player = p
    game.world.add_player(p)


def input_handler(brain, line):
    return _login_command_manager.input_handler(brain, line)


def init():
    _login_command_manager.add("login", login_command)
    _login_command_manager.add("quit", basic_commands.quit_command)
