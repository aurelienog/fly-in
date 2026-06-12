import pytest

from src.errors import InvalidSyntaxError
from src.parser.syntax_layer import (extract_metadata)


def test_extract_metadata_without_metadata() -> None:
    line, metadata = extract_metadata(
        "corridorA-tunnelB"
    )

    assert line == "corridorA-tunnelB"
    assert metadata is None


def test_extract_connection_metadata() -> None:
    line, metadata = extract_metadata(
        "corridorA-tunnelB "
        "[max_link_capacity=2]"
    )

    assert line == "corridorA-tunnelB"

    assert metadata == (
        "max_link_capacity=2"
    )


def test_extract_hub_metadata() -> None:
    line, metadata = extract_metadata(
        "corridorA 4 3 "
        "[zone=priority color=green "
        "max_drones=2]"
    )

    assert line == "corridorA 4 3"

    assert metadata == (
        "zone=priority "
        "color=green "
        "max_drones=2"
    )


def test_extract_metadata_empty_metadata() -> None:
    line, metadata = extract_metadata(
        "corridorA-tunnelB []"
    )

    assert line == "corridorA-tunnelB"
    assert metadata == ""


def test_extract_metadata_strip_spaces() -> None:
    line, metadata = extract_metadata(
        "  corridorA-tunnelB   "
        "[max_link_capacity=2]   "
    )

    assert line == "corridorA-tunnelB"
    assert metadata == "max_link_capacity=2"


def test_extract_metadata_unclosed_open_bracket() -> None:
    with pytest.raises(InvalidSyntaxError):
        extract_metadata(
            "corridorA-tunnelB "
            "[max_link_capacity=2"
        )


def test_extract_metadata_unopened_close_bracket() -> None:
    with pytest.raises(InvalidSyntaxError):
        extract_metadata(
            "corridorA-tunnelB "
            "max_link_capacity=2]"
        )


def test_extract_metadata_multiple_open_brackets() -> None:
    with pytest.raises(InvalidSyntaxError):
        extract_metadata(
            "corridorA "
            "[[max_link_capacity=2]]"
        )


def test_extract_metadata_close_before_open() -> None:
    with pytest.raises(InvalidSyntaxError):
        extract_metadata(
            "corridorA ]test["
        )
