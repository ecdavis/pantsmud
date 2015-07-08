"""
An extensible parser that can be used to validate user input.
"""

from pantsmud import command


STRING = "string"
WORD = "word"
INT = "int"


class ParseError(command.CommandError):
    """
    Raised when an error is found in a token string passed to a parser.
    """
    pass


class PatternError(Exception):
    """
    Raised when an error is found in a pattern passed to a parser.
    """
    pass


class Parser(object):
    """
    An extensible parsing object.

    Parsing works with three fundamental structures: token strings, token types and patterns.

    A token string is a string - typically user input - that contains an ordered collection of tokens. The tokens could
    be words, numbers, UUIDs, game objects or anything else that can be represented as or identified by a string.

    A token type is a key value pair where the key is the name of the token type and the value is a function which can
    parse the value of a token with that token type from the beginning of a token string.

    A pattern is an ordered collection of rules for reading tokens from a token string. Each token type referenced by
    the pattern is matched against the token string until either all token types have been successfully matched or a
    failure occurs.

    Adding custom token types to a parser is the primary method of extending it, as it allows a developer to add
    parsing functions which can read custom game objects from token strings. For instance,

    An example pattern:

        [("name", WORD), ("birth_year", INT), ("description", STRING)]

    WORD, INT and STRING are all token type names.

    An example token string which matches the above pattern:

        "Pants 5 A lightweight framework for writing asynchronous network application in Python."

    If we were to parse this string using the above pattern, we would get the result:

        {
            "name": "Pants",
            "birth_year": 2011,
            "description": "A lightweight framework for writing asynchronous network application in Python."
        }

    Token type parsing functions must take a single argument - the token string - and must return two values - the
    token value and the rest of the token string (i.e. the parsing function must remove the token value from the token
    string). If parsing fails, the parsing function must raise a ParseError.
    """
    def __init__(self):
        self._token_types = {}
        self.add_token_type(STRING, parse_string)
        self.add_token_type(WORD, parse_word)
        self.add_token_type(INT, parse_int)

    def add_token_type(self, type_name, type_func):
        """
        Add a token type to the parser.

        Raises a TypeError if type_func is not callable.
        """
        if not callable(type_func):
            raise TypeError("'type_func' must be callable.")
        self._token_types[type_name] = type_func

    def parse(self, pattern, token_string):
        """
        Parse a token string against the given pattern.

        Returns a dictionary of (token_name, token_value) pairs.

        Raises a ParseError if a token fails to match, or if there is any other error in the token string.
        Raises a PatternError if a type_name specified in the pattern is not found on the parser.
        """
        results = []
        for token_name, type_func in self._validate_pattern(pattern):
            if not token_string:
                raise ParseError("Not enough parameters supplied to command.")
            value, token_string = type_func(token_string)
            token_string = token_string.lstrip(' ')
            results.append((token_name, value))
        if token_string:
            raise ParseError("Too many parameters supplied to command.")
        return dict(results)

    def _validate_pattern(self, pattern):
        for token_name, type_name in pattern:
            if type_name not in self._token_types:
                raise PatternError("Token type '%s' in pattern '%r' not found on parser class '%s'" %
                                   (type_name, repr(pattern), self.__class__.__name__))
            yield (token_name, self._token_types[type_name])


def parse_string(token_string):
    """
    Parse a string from a token string.
    """
    return token_string, ''


def parse_word(token_string):
    """
    Parse a single word from a token string.
    """
    if ' ' in token_string:
        return token_string.split(' ', 1)
    else:
        return token_string, ''


def parse_int(params):
    """
    Parse a single integer from a token string.

    Raises a ParseError if the token value cannot be converted to an int.
    """
    if ' ' in params:
        value, rest = params.split(' ', 1)
    else:
        value, rest = params, ''
    try:
        return int(value), rest
    except ValueError:
        raise ParseError("Invalid parameter value: '%s'" % value)


_parser = Parser()
add_token_type = _parser.add_token_type
parse = _parser.parse
