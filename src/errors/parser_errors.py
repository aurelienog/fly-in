class ParseError(Exception):
    pass


class InvalidSyntaxError(ParseError):
    pass


class SemanticError(ParseError):
    pass
