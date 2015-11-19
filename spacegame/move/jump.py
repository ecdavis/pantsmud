from pantsmud.driver import error, parser

from spacegame import command


def jump_command(mobile, _, args):
    params = parser.parse([("link_name", parser.WORD)], args)
    start = mobile.node
    try:
        dest = start.get_link(params["link_name"]).dest
    except Exception:
        raise error.CommandError("No link '%s' exists." % params["link_name"])
    start.remove_mobile(mobile)
    dest.add_mobile(mobile)
    mobile.message("jump.success")


def init():
    command.add_command("jump", jump_command)
