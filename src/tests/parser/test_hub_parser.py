from __future__ import annotations
from ...parser.syntax_layer import parse_hub
from ...errors import InvalidSyntaxError
import pytest

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...parser.models import RawHub


def test_parse_valid_start_hub() -> None:

    start_content: str = "hub 0 0 [color=green]"
    start_type: str = "start_hub"

    raw_hub: RawHub = parse_hub(start_content, start_type)

    assert raw_hub.hub_type == start_type
    assert raw_hub.name == "hub"
    assert raw_hub.x == 0
    assert raw_hub.y == 0
    assert raw_hub.zone == "normal"
    assert raw_hub.color == "green"
    assert raw_hub.max_drones == 1


def test_parse_valid_end_hub() -> None:

    end_content: str = "goal 10 10 [color=yellow]"
    end_type: str = "end_hub"

    raw_hub: RawHub = parse_hub(end_content, end_type)

    assert raw_hub.hub_type == end_type
    assert raw_hub.name == "goal"
    assert raw_hub.x == 10
    assert raw_hub.y == 10
    assert raw_hub.zone == "normal"
    assert raw_hub.color == "yellow"
    assert raw_hub.max_drones == 1


def test_parse_valid_common_hub() -> None:

    common_content: str = "corridorA 4 3 [zone=priority color=green max_drones=2]"
    common_type: str = "common_hub"

    raw_hub: RawHub = parse_hub(common_content, common_type)

    assert raw_hub.hub_type == common_type
    assert raw_hub.name == "corridorA"
    assert raw_hub.x == 4
    assert raw_hub.y == 3
    assert raw_hub.zone == "priority"
    assert raw_hub.color == "green"
    assert raw_hub.max_drones == 2


def test_parse_empty_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("", "")


def test_parse_hub_empty_metadata() -> None:
    raw = parse_hub("hub 0 0 []", "common_hub")
    assert raw.zone == "normal"
    assert raw.color is None


def test_parse_invalid_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("corridorA A B [color=green 2]", "common_hub")


def test_parse_invalid_metadata_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("hub 0 0 [invalid=value]", "common_hub")

# start and end pueden tener metadatos que no sean color?
# porque al nivel semantico no tiene sentido
# caso especial a gestionar?
