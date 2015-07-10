"""
PantsMUD core exception classes.
"""

class BrainMissingInputHandlers(Exception):
    pass


class ZoneNotFound(Exception):
    pass


class NodeNotFound(Exception):
    pass


class LinkNotFound(Exception):
    pass


class LinkAlreadyExists(Exception):
    pass
