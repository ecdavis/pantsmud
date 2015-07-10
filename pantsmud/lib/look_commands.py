import logging

from pantsmud.driver import command, message, parser

log = logging.getLogger(__name__)


def look_node(node):
    return node.name


def look_mobiles(node):
    return [str(mobile.uuid) for mobile in node.mobiles]


def look_links(node):
    return [link.name for link in node.links]


def look_command(brain, cmd, args):
    log.debug(look_command.__name__)
    parser.parse([], args)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "node": look_node(brain.mobile.node),
        "links": look_links(brain.mobile.node),
        "mobiles": look_mobiles(brain.mobile.node)
    }
    brain.message("look", data)


def look_node_command(brain, cmd, args):
    log.debug(look_node_command.__name__)
    parser.parse([], args)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "node": look_node(brain.mobile.node)
    }
    brain.message("look.node", data)


def look_links_command(brain, cmd, args):
    log.debug(look_links_command.__name__)
    parser.parse([], args)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "links": look_links(brain.mobile.node)
    }
    brain.message("look.links", data)


def look_mobiles_command(brain, cmd, args):
    log.debug(look_mobiles_command.__name__)
    parser.parse([], args)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "mobiles": look_mobiles(brain.mobile.node)
    }
    brain.message("look.mobiles", data)


def brain_can_look(brain, cmd):
    if not brain.mobile:
        log.error("Brain '%s' executed command '%s' but has no mobile attached.", str(brain.uuid), cmd)
        return False
    if not brain.mobile.node:
        log.error("Brain '%s' executed command '%s' but its mobile '%s' has no node attached.",
                  str(brain.uuid), cmd, str(brain.mobile.uuid))
        return False
    return True


def init():
    command.add("look", look_command)
    command.add("look.node", look_node_command)
    command.add("look.links", look_links_command)
    command.add("look.mobiles", look_mobiles_command)
