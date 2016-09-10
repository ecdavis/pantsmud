import logging
import pants
import string
from pantsmud import game
from pantsmud.driver import session

log = logging.getLogger(__name__)


class GameConnection(pants.Stream):
    def on_connect(self):
        log.debug("on_connect: '%s'", self)
        self.read_delimiter = "\r\n"
        session.open_session(self)

    def on_read(self, line):
        log.debug("on_read: '%s'", self)
        line = line.strip(string.whitespace)
        if line:
            game.handle_input(session.get_session(self), line)

    def on_close(self):
        log.debug("on_close: '%s'", self)
        session.close_session(self)


class GameServer(pants.Server):
    def __init__(self, **kwargs):
        pants.Server.__init__(self, ConnectionClass=GameConnection, **kwargs)
