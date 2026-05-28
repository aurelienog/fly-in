from src.parser.syntax_layer import parse_hub
from src.errors import InvalidSyntaxError
from src.parser.models import RawHub

import pytest


def test_parse_valid_start_hub() -> None:

    start_content: str = "hub 0 0 [color=green]"
    start_type: str = "start_hub"

    raw_hub: RawHub = parse_hub(start_content, start_type, 42)

    assert raw_hub.hub_type == start_type
    assert raw_hub.name == "hub"
    assert raw_hub.x == 0
    assert raw_hub.y == 0
    assert raw_hub.zone == "normal"
    assert raw_hub.color == "green"
    assert raw_hub.max_drones == 1
    assert raw_hub.line == 42


def test_parse_valid_end_hub() -> None:

    end_content: str = "goal 10 10 [color=yellow]"
    end_type: str = "end_hub"

    raw_hub: RawHub = parse_hub(end_content, end_type, 42)

    assert raw_hub.hub_type == end_type
    assert raw_hub.name == "goal"
    assert raw_hub.x == 10
    assert raw_hub.y == 10
    assert raw_hub.zone == "normal"
    assert raw_hub.color == "yellow"
    assert raw_hub.max_drones == 1
    assert raw_hub.line == 42


def test_parse_valid_common_hub() -> None:

    common_content: str = "corridorA 4 3 [zone=priority color=green max_drones=2]"
    common_type: str = "common_hub"

    raw_hub: RawHub = parse_hub(common_content, common_type, 42)

    assert raw_hub.hub_type == common_type
    assert raw_hub.name == "corridorA"
    assert raw_hub.x == 4
    assert raw_hub.y == 3
    assert raw_hub.zone == "priority"
    assert raw_hub.color == "green"
    assert raw_hub.max_drones == 2
    assert raw_hub.line == 42


def test_parse_empty_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("", "", 42)


def test_parse_hub_empty_metadata() -> None:
    raw = parse_hub("hub 0 0 []", "common_hub", 42)
    assert raw.zone == "normal"
    assert raw.color is None


def test_parse_invalid_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("corridorA A B [color=green 2]", "common_hub", 42)


def test_parse_invalid_metadata_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("hub 0 0 [invalid=value]", "common_hub", 42)


def test_hub_name_cannot_contain_dash() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_hub("hub-A 0 2", "hub", 42)
