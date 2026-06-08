from .lexer import tokenize_lines
from .syntax_layer.dispatcher import parse_raw_network
from .semantic_layer import validate_network, validate_reachability

from .builders import build_network, build_drones
from ..domain import Network, Drone

from .models import RawNetwork


def parse_simulation(source: str) -> tuple[Network, list[Drone]]:
    """Parse a complete simulation from a raw text source.

    The function performs the full pipeline required to transform an
    input text into a validated simulation model. This includes tokenizing,
    parsing, semantic validation, and construction of the final domain
    objects.

    Args:
        source: Raw simulation input text.

    Returns:
        A tuple containing:
            - The constructed and validated network.
            - The list of initialized drones for the simulation.
    """

    tokens: list[tuple[int, str, str]] = tokenize_lines(source)
    raw_network: RawNetwork = parse_raw_network(tokens)
    validate_network(raw_network)
    network = build_network(raw_network)
    drones = build_drones(raw_network, network)

    validate_reachability(network)

    return (network, drones)
