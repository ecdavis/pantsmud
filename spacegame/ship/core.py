from pantsmud.driver import auxiliary, parser

from spacegame import command


SHIP_AUX = "ship"


# TODO Use a vector library.
class ShipAux(object):
    def __init__(self):
        self.position = (0, 0, 0)

    def load_data(self, data):
        pass

    def save_data(self):
        return None


def message_ship_info(mobile):
    data = {
        "position": list(mobile.aux[SHIP_AUX].position)
    }
    mobile.message("ship.info", data)

def command_ship_info(mobile, _, args):
    parser.parse([], args)
    message_ship_info(mobile)


def init():
    auxiliary.install(auxiliary.AUX_TYPE_MOBILE, SHIP_AUX, ShipAux)
    command.add_command("ship.info", command_ship_info)
