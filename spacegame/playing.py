from pantsmud.driver import hook, parser

from spacegame import command, user


def save_mobile(mobile):
    if mobile.brain.is_user:
        user.save_player(mobile)


def save_command(mobile, _, args):
    save_mobile(mobile)


def quit_command(mobile, _, args):
    parser.parse([], args)
    save_mobile(mobile)
    mobile.brain.close()


def shutdown_command(mobile, _, args):
    parser.parse([], args)
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command.add_command("save", save_command)
    command.add_command("quit", quit_command)
    command.add_command("shutdown", shutdown_command)
