import logging

from pantsmud import message

log = logging.getLogger(__name__)


class CommandManager(object):
    def __init__(self, name):
        self.name = name
        self._commands = {}  # name: func

    def add(self, name, func):
        assert name not in self._commands
        log.debug("Adding new command: '%s', func '%s', manager '%s'", name, func.__name__, self.name)
        self._commands[name] = func

    def exists(self, name):
        return name in self._commands

    def run(self, brain, cmd, args):
        if cmd not in self._commands:
            raise Exception("TODO")  # TODO
        try:
            self._commands[cmd](brain, cmd, args)
        except Exception:
            log.exception("Unhandled exception in command: '%s', func '%s', manager '%s",
                          cmd, self._commands[cmd].__name__, self.name)

    def input_handler(self, brain, line):
        line = line.rstrip('\r\n')
        if ' ' in line:
            cmd, args = line.split(' ', 1)
        else:
            cmd, args = line, ''
        if self.exists(cmd):
            self.run(brain, cmd, args)
        else:
            message.command_notfound(brain, cmd, args)


_command_manager = CommandManager(__name__)


def add(name, func):
    return _command_manager.add(name, func)


def exists(name):
    return _command_manager.exists(name)


def run(brain, cmd, args):
    return _command_manager.run(brain, cmd, args)


def input_handler(brain, line):
    return _command_manager.input_handler(brain, line)
