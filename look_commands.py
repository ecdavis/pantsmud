import logging

from pantsmud import command

log = logging.getLogger(__name__)


def look_room(room):
    return room.name


def look_players(room):
    return [str(player.uuid) for player in room.players]


def look_links(room):
    return [link.name for link in room.links]


def look_command(brain, cmd, args):
    log.debug(look_command.__name__)
    if not brain_can_look(brain, cmd):
        brain.message("command.fail", {"command": cmd, "parameters": args, "reason": "internal server error"})
        return
    data = {
        "room": look_room(brain.player.room),
        "links": look_links(brain.player.room),
        "players": look_players(brain.player.room)
    }
    brain.message("look", data)


def look_room_command(brain, cmd, args):
    log.debug(look_room_command.__name__)
    if not brain_can_look(brain, cmd):
        brain.message("command.fail", {"command": cmd, "parameters": args, "reason": "internal server error"})
        return
    data = {
        "room": look_room(brain.player.room)
    }
    brain.message("look.room", data)


def look_links_command(brain, cmd, args):
    log.debug(look_links_command.__name__)
    if not brain_can_look(brain, cmd):
        brain.message("command.fail", {"command": cmd, "parameters": args, "reason": "internal server error"})
        return
    data = {
        "links": look_links(brain.player.room)
    }
    brain.message("look.links", data)


def look_players_command(brain, cmd, args):
    log.debug(look_players_command.__name__)
    if not brain_can_look(brain, cmd):
        brain.message("command.fail", {"command": cmd, "parameters": args, "reason": "internal server error"})
        return
    data = {
        "players": look_players(brain.player.room)
    }
    brain.message("look.players", data)


def brain_can_look(brain, cmd):
    if not brain.player:
        log.error("Brain '%s' executed command '%s' but has no player attached.", str(brain.uuid), cmd)
        return False
    if not brain.player.room:
        log.error("Brain '%s' executed command '%s' but its player '%s' has no room attached.",
                  str(brain.uuid), cmd, str(brain.player.uuid))
        return False
    return True


def init():
    command.add("look", look_command)
    command.add("look.room", look_room_command)
    command.add("look.links", look_links_command)
    command.add("look.players", look_players_command)
