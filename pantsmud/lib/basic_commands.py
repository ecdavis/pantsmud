import logging

from pantsmud.driver import command, parser, hook


def say_command(brain, cmd, args):
    logging.debug("say_command")
    params = parser.parse([("sentence", parser.STRING)], args.split(' '))
    for p in brain.mobile.node.mobiles:
        p.brain.message("mobile.say", {"mobile": str(brain.mobile.uuid), "text": params["sentence"]})


def tell_command(brain, cmd, args):
    target, message = parser.parse((("target", parser.PLAYER), ("message", parser.STRING)), args)
    target.message("tell", {"from": brain.mobile.name, "message": message})


def move_command(brain, cmd, args):
    logging.debug("move_command")
    params = parser.parse([("link_name", parser.WORD)], args)
    link_name = params["link_name"]
    try:
        dest = brain.mobile.node.get_link(link_name).dest
    except Exception:
        raise command.CommandError("No link '%s' exists." % link_name)
    brain.mobile.node.remove_mobile(brain.mobile)
    dest.add_mobile(brain.mobile)


def quit_command(brain, cmd, args):
    logging.debug("quit_command")
    parser.parse([], args)
    brain.close()


def shutdown_command(brain, cmd, args):
    parser.parse([], args)
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command.add("say", say_command)
    command.add("move", move_command)
    command.add("quit", quit_command)
    command.add("shutdown", shutdown_command)
