import spacegame.ship.core
import spacegame.ship.thrusters
import spacegame.ship.update


def init():
    spacegame.ship.core.init()
    spacegame.ship.thrusters.init()


def start():
    spacegame.ship.update.start()
