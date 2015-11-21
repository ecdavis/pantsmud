from pantsmud.driver import hook, parser
from pantsmud.world import node

from spacegame import command
from spacegame.ship import core


def scan_node(node):
    return {"name": node.name, "id": str(node.uuid)}


def scan_link(link):
    data = {
        "id": str(link.uuid),
        "name": link.name
    }
    return data


def scan_links(node):
    return [scan_link(link) for link in node.links]


def scan_mobile(mobile):
    data = {
        "id": str(mobile.uuid),
        "ship": core.get_ship_info(mobile)
    }
    return data


def scan_mobiles(node):
    return [scan_mobile(mobile) for mobile in node.mobiles]


def message_scanner_scan(mobile, node):
    data = {
        "node": scan_node(node),
        "links": scan_links(node),
        "mobiles": scan_mobiles(node)
    }
    mobile.message("scanner.scan", data)


def hook_scan_on_add(_, node, mobile):
    message_scanner_scan(mobile, node)


def command_scanner_scan(mobile, _, args):
    parser.parse([], args)
    message_scanner_scan(mobile, mobile.node)


def init():
    hook.add(node.HOOK_NODE_ADD_MOBILE, hook_scan_on_add)
    command.add_command("scanner.scan", command_scanner_scan)
