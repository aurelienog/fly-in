from .lexer import tokenize_lines
from .syntax_layer.dispatcher import parse_raw_network
from .semantic_layer import validate_network

from .builders import build_network, build_drones
from ..domain import Network, Drone

from .models import RawNetwork


def parse_simulation(source: str) -> tuple[Network, list[Drone]]:

    tokens: list[tuple[int, str, str]] = tokenize_lines(source)
    raw_network: RawNetwork = parse_raw_network(tokens)
    validate_network(raw_network)
    network = build_network(raw_network)
    drones = build_drones(raw_network, network)
    return (network, drones)
