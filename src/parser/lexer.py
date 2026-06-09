
from ..errors import ParseError


def tokenize_lines(text: str) -> list[tuple[int, str, str]]:
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
