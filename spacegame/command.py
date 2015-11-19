import logging

from pantsmud.driver import command, message

log = logging.getLogger(__name__)


class GameCommandManager(command.CommandManager):
    def run(self, brain, cmd, args):
        command.CommandManager.run(self, brain.mobile, cmd, args)

    def input_handler(self, brain, line):
        if not brain.mobile:
            log.error("Brain '%s' has game input handler but does not have a mobile attached.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        if not brain.mobile.node:
            log.error("Brain '%s' has game input handler but mobile '%s' does not have a node.",
                      str(brain.uuid), str(brain.mobile.uuid))
            message.command_internal_error(brain)
            return
        return command.CommandManager.input_handler(self, brain, line)

_game_command_manager = GameCommandManager(__name__)
add_command = _game_command_manager.add
command_exists = _game_command_manager.exists
command_input_handler = _game_command_manager.input_handler
