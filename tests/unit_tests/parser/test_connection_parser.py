from src.parser.syntax_layer import parse_connection
from src.errors import InvalidSyntaxError
from src.parser.models import RawConnection

import pytest


def test_parse_valid_connection() -> None:

    content: str = "corridorA-tunnelB [max_link_capacity=2]"

    raw_connection: RawConnection = parse_connection(content, 42)

    assert raw_connection.a == "corridorA"
    assert raw_connection.b == "tunnelB"
    assert raw_connection.max_link_capacity == 2
    assert raw_connection.line == 42


def test_parse_connection_with_spaces() -> None:
    raw_connection = parse_connection("  corridorA  -  tunnelB  ", 42)

    assert raw_connection.a == "corridorA"
    assert raw_connection.b == "tunnelB"
    assert raw_connection.max_link_capacity == 1
    assert raw_connection.line == 42


def test_parse_connection_missing_left_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("-tunnelB", 42)


def test_parse_connection_missing_right_hub() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("tunnelB-", 42)


def test_parse_empty_connection() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("", 42)


def test_parse_connection_without_dash() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("corridorA", 42)


def test_parse_connection_empty_metadata() -> None:
    raw_connection = parse_connection("corridorA-tunnelB []", 42)

    assert raw_connection.a == "corridorA"
    assert raw_connection.b == "tunnelB"
    assert raw_connection.max_link_capacity == 1


def test_parse_invalid_metadata_connection() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("roof1-roof2 [invalid=value]", 42)


def test_parse_connection_unknown_metadata_key() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("a-b [max_link_capacity=2,foo=1]", 42)


def test_parse_connection_invalid_name_contain_dash() -> None:
    with pytest.raises(InvalidSyntaxError):
        parse_connection("roof1-tunnel-B", 42)
