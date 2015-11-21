from pantsmud.driver import game


POSITION_UPDATE_TICK = 0.1


def update_position(mobile, seconds):
    ship = mobile.aux["ship"]
    thrusters = mobile.aux["thrusters"]
    ship.position = (round(ship.position[0] + (thrusters.velocity()[0] * seconds), 3),
                     round(ship.position[1] + (thrusters.velocity()[1] * seconds), 3),
                     round(ship.position[2] + (thrusters.velocity()[2] * seconds), 3))


def update_position_cycle():
    for mobile in game.world.mobiles.values():
        update_position(mobile, POSITION_UPDATE_TICK)


def start():
    game.engine.cycle(POSITION_UPDATE_TICK, update_position_cycle)
