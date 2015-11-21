import spacegame.brain_handler
import spacegame.login
import spacegame.move
import spacegame.playing
import spacegame.info
import spacegame.ship


def init():
    # Core init
    spacegame.brain_handler.init()
    spacegame.login.init()
    # Command init
    spacegame.playing.init()
    spacegame.move.init()
    spacegame.info.init()
    spacegame.ship.init()


def start():
    spacegame.ship.start()
