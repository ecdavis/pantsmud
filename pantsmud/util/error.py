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


class CommandError(Exception):
    pass


class CommandFail(Exception):
    pass


class ParseError(CommandError):
    """
    Raised when an error is found in a token string passed to a parser.
    """
    pass


class PatternError(Exception):
    """
    Raised when an error is found in a pattern passed to a parser.
    """
    pass
