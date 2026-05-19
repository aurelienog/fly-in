from __future__ import annotations

import pytest

from ...errors import InvalidSyntaxError
from ...parser.syntax_layer.metadata_parser import (parse_metadata)


def test_parse_metadata_none() -> None:
    meta = parse_metadata(None)

    assert meta == {}


def test_parse_metadata_empty_string() -> None:
    meta = parse_metadata("")

    assert meta == {}


def test_parse_connection_metadata() -> None:
    meta = parse_metadata(
        "max_link_capacity=2"
    )

    assert meta == {
        "max_link_capacity": "2",
    }


def test_parse_hub_metadata() -> None:
    meta = parse_metadata(
        "zone=priority "
        "color=green "
        "max_drones=2"
    )

    assert meta == {
        "zone": "priority",
        "color": "green",
        "max_drones": "2",
    }


def test_parse_metadata_missing_equal() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_metadata(
            "max_link_capacity"
        )


def test_parse_metadata_empty_key() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_metadata(
            "=2"
        )


def test_parse_metadata_empty_value() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_metadata(
            "max_link_capacity="
        )


def test_parse_metadata_duplicate_key() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_metadata(
            "color=green "
            "color=red"
        )
