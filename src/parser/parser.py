from .lexer import tokenize_lines
from .syntax_layer.dispatcher import parse_raw_network
from .semantic_layer import validate_network
from .builders import build_network
from ..domain import Network
from .models import RawNetwork


def parse_network(source: str) -> Network:

    tokens: list[tuple[int, str, str]] = tokenize_lines(source)
    raw_network: RawNetwork = parse_raw_network(tokens)
    validate_network(raw_network)

    return build_network(raw_network)
