from pantsmud.driver import error, parser

from spacegame import command


def who_mobile_command(mobile, _, args):
    params = parser.parse([("mobile_uuid", parser.UUID)], args)
    if not params["mobile_uuid"] in mobile.world.mobiles:
        raise error.CommandError("No mobile '%s' exists." % str(params["mobile_uuid"]))
    else:
        whom = mobile.world.mobiles[params["mobile_uuid"]]
        mobile.message("who.mobile", {
            "uuid": str(whom.uuid)
        })


def who_list_command(mobile, _, args):
    parser.parse([], args)
    mobs = [str(u) for u in mobile.world.mobiles]
    mobile.message("who.list", {"mobiles": mobs})


def init():
    command.add_command("who.mobile", who_mobile_command)
    command.add_command("who.list", who_list_command)
