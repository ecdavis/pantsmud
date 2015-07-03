import logging

import pants

from pantsmud import game
from pantsmud.user import session

log = logging.getLogger(__name__)


class LineStream(pants.Stream):
    def on_connect(self):
        log.debug("on_connect: '%s'", self)
        self.read_delimiter = "\r\n"
        session.open_session(self)

    def on_read(self, line):
        log.debug("on_read: '%s'", self)
        game.handle_input(session.get_session(self), line)

    def on_close(self):
        log.debug("on_close: '%s'", self)
        session.close_session(self)
