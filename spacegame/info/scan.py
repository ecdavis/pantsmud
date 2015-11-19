from pantsmud.driver import hook, parser
from pantsmud.world import node

from spacegame import command


def scan_hook(_, node, mobile):
    scan(node, mobile)

def scan(node, mobile):
    data = {
        "node": scan_node(node),
        "links": scan_links(node),
        "mobiles": scan_mobiles(node)
    }
    mobile.message("scan", data)


def scan_node(node):
    return node.name


def scan_links(node):
    return [link.name for link in node.links]


def scan_mobiles(node):
    return [str(mobile.uuid) for mobile in node.mobiles]


def scan_command(mobile, _, args):
    parser.parse([], args)
    scan(mobile.node, mobile)


def init():
    command.add_command("scan", scan_command)
    hook.add(node.HOOK_NODE_ADD_MOBILE, scan_hook)
