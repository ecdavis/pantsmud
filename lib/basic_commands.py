import logging

from pantsmud import command, hook


def say_command(brain, cmd, args):
    logging.debug("say_command")
    for p in brain.mobile.node.mobiles:
        p.brain.message("mobile.say", {"mobile": str(brain.mobile.uuid), "text": args})


def move_command(brain, cmd, args):
    logging.debug("move_command")
    if not args:
        brain.write_line("Too few arguments. Usage: move <link>")
        return
    if ' ' in args:
        brain.write_line("Too many arguments. Usage: move <link>")
        return
    link_name = args.lower()
    try:
        dest = brain.mobile.node.get_link(link_name).dest
    except Exception:
        brain.write_line("No link '%s' exists." % link_name)
        return
    brain.mobile.node.remove_mobile(brain.mobile)
    dest.add_mobile(brain.mobile)


def quit_command(brain, cmd, args):
    logging.debug("quit_command")
    brain.close()


def shutdown_command(brain, cmd, args):
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command.add("say", say_command)
    command.add("move", move_command)
    command.add("quit", quit_command)
    command.add("shutdown", shutdown_command)
