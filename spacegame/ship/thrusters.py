from pantsmud.driver import auxiliary, error, parser

from spacegame import command


THRUSTERS_AUX = "thrusters"


# TODO Use a vector library.
class ThrustersAux(object):
    def __init__(self):
        self.max_speed = 10.0
        self.direction = (1.0, 0, 0)
        self.power = 0.0

    def load_data(self, data):
        pass

    def save_data(self):
        return None

    def speed(self):
        return self.power * self.max_speed

    def velocity(self):
        return (round(self.direction[0]*self.speed(), 3),  # X
                round(self.direction[1]*self.speed(), 3),  # Y
                round(self.direction[2]*self.speed(), 3))  # Z


def message_thrusters_info(mobile):
    thrusters = mobile.aux[THRUSTERS_AUX]
    data = {
        "thrusters.direction": list(thrusters.direction),
        "thrusters.power": thrusters.power
    }
    mobile.message("thrusters.info", data)


def command_thrusters_info(mobile, _, args):
    parser.parse([], args)
    message_thrusters_info(mobile)


def command_thrusters_direction(mobile, _, args):
    params = parser.parse([("x", parser.FLOAT), ("y", parser.FLOAT), ("z", parser.FLOAT)], args)
    x = round(params["x"], 3)
    y = round(params["y"], 3)
    z = round(params["z"], 3)
    direction_vector = (x, y, z)
    if x > 1.0 or y > 1.0 or z > 1.0:
        raise error.CommandError("Invalid direction vector '%s'." % str(direction_vector))
    if abs(1.0 - sum((abs(x), abs(y), abs(z)))) > 0.001:
        raise error.CommandError("Invalid direction vector '%s'." % str(direction_vector))
    mobile.aux[THRUSTERS_AUX].direction = direction_vector
    message_thrusters_info(mobile)


def command_thrusters_power(mobile, _, args):
    params = parser.parse([("power", parser.FLOAT)], args)
    power = round(params["power"], 3)
    if power < 0.0 or power > 1.0:
        raise error.CommandError("Invalid power value '%s'." % str(power))
    mobile.aux[THRUSTERS_AUX].power = power
    message_thrusters_info(mobile)


def init():
    auxiliary.install(auxiliary.AUX_TYPE_MOBILE, THRUSTERS_AUX, ThrustersAux)
    command.add_command("thrusters.info", command_thrusters_info)
    command.add_command("thrusters.direction", command_thrusters_direction)
    command.add_command("thrusters.power", command_thrusters_power)
