class ParseError(Exception):
    """Base exception raised for errors encountered while parsing."""
    pass


class InvalidSyntaxError(ParseError):
    """Raised when the input contains invalid or malformed syntax."""
    pass


class SemanticError(ParseError):
    """Raised when the input is syntactically valid but semantically invalid."""
    pass
