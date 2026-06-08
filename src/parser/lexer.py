
from ..errors import ParseError


def tokenize_lines(text: str) -> list[tuple[int, str, str]]:
    """Tokenize a raw text input into structured (line, keyword, content) tuples.

    The function processes a line-based format where each meaningful line
    must follow the pattern ``<keyword>: <content>``. Empty lines and comment
    lines starting with ``#`` are ignored.

    Args:
        text: Raw input text to tokenize.

    Returns:
        A list of tokens, each represented as a tuple:
            - line number in the original input (starting at 1)
            - keyword extracted from the line
            - content associated with the keyword

    Raises:
        ParseError: If a line does not follow the expected format,
            or if keyword/content is missing.
    """
    tokens = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            raise ParseError(
                f"Line {line_number}: expected '<keyword>: <content>'"
            )

        keyword, content = line.split(":", 1)
        keyword = keyword.strip()
        content = content.strip()

        if not keyword:
            raise ParseError(f"Line {line_number}: missing keyword")

        if not content:
            raise ParseError(f"Line {line_number}: missing content")

        tokens.append((line_number, keyword, content))
    return tokens
