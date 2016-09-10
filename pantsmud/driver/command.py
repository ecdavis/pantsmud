import logging
import string
from pantsmud.util import error, message

log = logging.getLogger(__name__)
valid_input_characters = string.ascii_letters + string.digits + string.punctuation + ' '


_command_manager = None


class CommandManager(object):
    def __init__(self, name):
        self.name = name
        self._commands = {}  # name: func

    def add(self, name, func):
        # There's a direct relationship between command names and user input, hence why we validate like this.
        if name is '':
            raise ValueError("'name' cannot be an empty string.")
        if not name:
            raise TypeError("'name' must exist.")
        if any((c not in valid_input_characters for c in name)):
            raise ValueError("'name' can only contain valid input characters.")
        if any((c in name for c in string.whitespace)):
            raise ValueError("'name' cannot contain whitespace.")
        # Better to catch this here than when the command gets called at runtime.
        if not callable(func):
            raise TypeError("'func' must be callable.")
        assert name not in self._commands
        log.debug("Adding new command: '%s', func '%s', manager '%s'", name, func.__name__, self.name)
        self._commands[name] = func

    def exists(self, name):
        return name in self._commands

    def run(self, actor, cmd, args):
        if not actor:
            raise TypeError("'actor' must exist.")
        if not actor.environment:
            raise ValueError("'actor' must be added to an environment before it can run commands.")
        if cmd not in self._commands:
            raise KeyError("Command '%s' does not exist in command manager '%s'" % (cmd, self.name))
        try:
            self._commands[cmd](actor, cmd, args)
        except error.CommandError:
            raise
        except error.CommandFail:
            raise
        except Exception:  # Catch Exception here because we have no control over what command code will throw.
            log.exception("Unhandled exception in command: '%s', func '%s', manager '%s'",
                          cmd, self._commands[cmd].__name__, self.name)

    def input_handler(self, actor, line):
        if not line:
            return
        line = line.rstrip(string.whitespace)
        if not line:
            return
        if line[0] not in string.letters:
            message.command_invalid_input(actor, line)
            return
        if any((c not in valid_input_characters for c in line)):
            message.command_invalid_input(actor, line)
            return
        if ' ' in line:
            cmd, args = line.split(' ', 1)
        else:
            cmd, args = line, ''
        # TODO validate/clean args?
        if self.exists(cmd):
            try:
                self.run(actor, cmd, args)
            except error.CommandError as e:
                message.command_error(actor, cmd, args, e.message)
            except error.CommandFail as e:
                message.command_fail(actor, cmd, args, e.message)
        else:
            message.command_not_found(actor, cmd, args)


def add_command(name, func):
    return _command_manager.add(name, func)


def command_exists(name):
    return _command_manager.exists(name)


def command_input_handler(actor, line):
    return _command_manager.input_handler(actor, line)


def init():
    global _command_manager
    _command_manager = CommandManager(__name__)
