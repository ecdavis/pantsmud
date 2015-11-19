import logging

from pantsmud.driver import game, message, parser
from pantsmud.driver import command as cmd  # to avoid clashing with spacegame command. blech.
from pantsmud.world import mobile

from spacegame import command, user

log = logging.getLogger(__name__)


class LoginCommandManager(cmd.CommandManager):
    def input_handler(self, brain, line):
        if not brain.is_user:
            log.error("Brain '%s' has login input handler but it is not a user.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        if brain.mobile:
            log.error("Brain '%s' has login input handler it already has a player '%s'.",
                      str(brain.uuid), str(brain.mobile.uuid))
            message.command_internal_error(brain)
            return
        return cmd.CommandManager.input_handler(self, brain, line)


_login_command_handler = LoginCommandManager(__name__)
login_input_handler = _login_command_handler.input_handler


def register_command(brain, cmd, args):
    parser.parse([], args)
    u = user.User()
    p = mobile.Mobile()
    u.player_uuid = p.uuid
    user.save_user(u)
    user.save_player(p)
    brain.message("register.success", {"uuid": str(u.uuid)})


def login_command(brain, cmd, args):
    params = parser.parse([("uuid", parser.UUID)], args)
    user_uuid = params["uuid"]
    if not user.user_exists(user_uuid):
        log.debug("login failed due to non-existent user")
        brain.message("login.fail")
        return
    u = user.load_user(user_uuid)
    if not u.player_uuid or not user.player_exists(u.player_uuid):
        log.debug("login failed due to non-existent player")
        brain.message("login.fail")
        return
    p = user.load_player(u.player_uuid)
    brain.message("login.success")
    brain.replace_input_handler(command.command_input_handler, "playing")
    p.attach_brain(brain)
    game.world.add_mobile(p)


def quit_command(brain, cmd, args):
    parser.parse([], args)
    brain.close()


def init():
    _login_command_handler.add("register", register_command)
    _login_command_handler.add("login", login_command)
    _login_command_handler.add("quit", quit_command)
