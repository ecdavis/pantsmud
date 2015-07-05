import logging
import string

import pants

from pantsmud import game
from pantsmud.user import session

log = logging.getLogger(__name__)

_server = None


class LineStream(pants.Stream):
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


def init():
    global _server
    _server = pants.Server(LineStream)
    _server.listen(4040)
