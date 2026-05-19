import pytest

from ...parser.syntax_layer.dispatcher import parse_raw_network
from ...errors import ParseError


def test_nb_drones_must_be_first_line() -> None:

    tokens = [
        (1, "hub", "roof1 3 4"),
        (2, "nb_drones", "5")
    ]

    with pytest.raises(ParseError):
        parse_raw_network(tokens)
