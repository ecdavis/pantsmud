from pantsmud.driver import parser

from spacegame import command


def broadcast_local_command(mobile, _, args):
    params = parser.parse([("message", parser.STRING)], args)
    node = mobile.node
    for m in node.mobiles:
        m.message("broadcast.local", {"mobile_from": str(mobile.uuid), "message": params["message"]})


def broadcast_global_command(mobile, _, args):
    params = parser.parse([("message", parser.STRING)], args)
    world = mobile.world
    for m in (world.mobiles[u] for u in world.mobiles):  # TODO bring this pattern in line with zone/node properties
        m.message("broadcast.global", {"mobile_from": str(mobile.uuid), "message": params["message"]})


def broadcast_private_command(mobile, _, args):
    params = parser.parse([("mobile_uuid", parser.UUID), ("message", parser.STRING)], args)
    target = mobile.world.mobiles[params["mobile_uuid"]]
    data = {
        "mobile_from": str(mobile.uuid),
        "mobile_to": str(target.uuid),
        "message": params["message"]
    }
    target.message("broadcast.private", data)
    mobile.message("broadcast.private", data)


def init():
    command.add_command("broadcast.local", broadcast_local_command)
    command.add_command("broadcast.global", broadcast_global_command)
    command.add_command("broadcast.private", broadcast_private_command)
