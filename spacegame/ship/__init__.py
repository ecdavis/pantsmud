import spacegame.ship.core
import spacegame.ship.broadcast
import spacegame.ship.thrusters
import spacegame.ship.scanner
import spacegame.ship.update


def init():
    spacegame.ship.core.init()
    spacegame.ship.broadcast.init()
    spacegame.ship.thrusters.init()
    spacegame.ship.scanner.init()


def start():
    spacegame.ship.update.start()
