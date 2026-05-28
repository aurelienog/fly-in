from src.parser.lexer import tokenize_lines
from src.errors import ParseError

from textwrap import dedent
import pytest


def test_tokenize_valid_lines() -> None:
    text = dedent("""\
        nb_drones: 5
        start_hub: hub 0 0 [color=green]
        end_hub: goal 10 10 [color=yellow]
        hub: roof1 3 4 [zone=restricted color=red]
        connection: hub-roof1
    """)

    tokenized_text = tokenize_lines(text)

    assert len(tokenized_text) == 5

    assert tokenized_text[0] == (1, "nb_drones", "5")

    assert tokenized_text[1] == (2, "start_hub", "hub 0 0 [color=green]")

    assert tokenized_text[4] == (5, "connection", "hub-roof1")


def test_tokenize_ignores_empty_lines() -> None:
    text = dedent("""

        nb_drones: 5


        hub: roof1 3 4
    """)

    tokenized_text = tokenize_lines(text)

    assert len(tokenized_text) == 2

    assert tokenized_text[0] == (
        3,
        "nb_drones",
        "5",
    )

    assert tokenized_text[1] == (
        6,
        "hub",
        "roof1 3 4",
    )


def test_tokenize_ignores_comment_lines() -> None:
    text = dedent("""# comment
        nb_drones: 5
        # another comment
        hub: roof1 3 4
    """)

    tokenized_text = tokenize_lines(text)

    assert len(tokenized_text) == 2

    assert tokenized_text[0] == (
        2,
        "nb_drones",
        "5",
    )

    assert tokenized_text[1] == (
        4,
        "hub",
        "roof1 3 4",
    )


def test_tokenize_strips_spaces() -> None:
    text = dedent("""\
        nb_drones   :    5
            hub    :    roof1 3 4
    """)

    tokenized_text = tokenize_lines(text)

    assert len(tokenized_text) == 2

    assert tokenized_text[0] == (
        1,
        "nb_drones",
        "5",
    )

    assert tokenized_text[1] == (
        2,
        "hub",
        "roof1 3 4",
    )


def test_tokenize_preserves_content_after_first_colon() -> None:
    text = dedent("""\
        metadata: value:another
    """)

    tokenized_text = tokenize_lines(text)

    assert len(tokenized_text) == 1

    assert tokenized_text[0] == (
        1,
        "metadata",
        "value:another",
    )


def test_tokenize_raises_when_missing_colon() -> None:
    text = dedent("""\
        nb_drones 5
    """)

    with pytest.raises(ParseError) as exc_info:
        tokenize_lines(text)

    assert (
        str(exc_info.value)
        == "Line 1: expected '<keyword>: <content>'"
    )


def test_tokenize_raises_when_keyword_is_missing() -> None:
    text = dedent("""\
        : value
    """)

    with pytest.raises(ParseError) as exc_info:
        tokenize_lines(text)

    assert str(exc_info.value) == "Line 1: missing keyword"


def test_tokenize_raises_when_content_is_missing() -> None:
    text = dedent("""\
        nb_drones:
    """)

    with pytest.raises(ParseError) as exc_info:
        tokenize_lines(text)

    assert str(exc_info.value) == "Line 1: missing content"


def test_tokenize_raises_with_correct_line_number() -> None:
    text = dedent("""\
        nb_drones: 5
        hub roof1 3 4
    """)

    with pytest.raises(ParseError) as exc_info:
        tokenize_lines(text)

    assert (
        str(exc_info.value)
        == "Line 2: expected '<keyword>: <content>'"
    )


def test_tokenize_returns_empty_list_for_empty_text() -> None:
    text = ""

    tokenized_text = tokenize_lines(text)

    assert tokenized_text == []


def test_tokenize_returns_empty_list_for_only_comments_and_spaces() -> None:
    text = dedent("""\
        # comment

            # another
    """)

    tokenized_text = tokenize_lines(text)

    assert tokenized_text == []
