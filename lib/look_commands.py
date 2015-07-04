import logging

from pantsmud import command, message

log = logging.getLogger(__name__)


def look_room(room):
    return room.name


def look_mobiles(room):
    return [str(mobile.uuid) for mobile in room.mobiles]


def look_links(room):
    return [link.name for link in room.links]


def look_command(brain, cmd, args):
    log.debug(look_command.__name__)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "room": look_room(brain.mobile.room),
        "links": look_links(brain.mobile.room),
        "mobiles": look_mobiles(brain.mobile.room)
    }
    brain.message("look", data)


def look_room_command(brain, cmd, args):
    log.debug(look_room_command.__name__)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "room": look_room(brain.mobile.room)
    }
    brain.message("look.room", data)


def look_links_command(brain, cmd, args):
    log.debug(look_links_command.__name__)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "links": look_links(brain.mobile.room)
    }
    brain.message("look.links", data)


def look_mobiles_command(brain, cmd, args):
    log.debug(look_mobiles_command.__name__)
    if not brain_can_look(brain, cmd):
        message.command_fail(brain, cmd, args)
        return
    data = {
        "mobiles": look_mobiles(brain.mobile.room)
    }
    brain.message("look.mobiles", data)


def brain_can_look(brain, cmd):
    if not brain.mobile:
        log.error("Brain '%s' executed command '%s' but has no mobile attached.", str(brain.uuid), cmd)
        return False
    if not brain.mobile.room:
        log.error("Brain '%s' executed command '%s' but its mobile '%s' has no room attached.",
                  str(brain.uuid), cmd, str(brain.mobile.uuid))
        return False
    return True


def init():
    command.add("look", look_command)
    command.add("look.room", look_room_command)
    command.add("look.links", look_links_command)
    command.add("look.mobiles", look_mobiles_command)
