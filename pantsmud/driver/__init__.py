from pantsmud.driver import auxiliary, command, hook, parser, session


def init():
    auxiliary.init()
    command.init()
    hook.init()
    parser.init()
    session.init()
