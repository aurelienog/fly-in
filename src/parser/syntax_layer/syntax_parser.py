
from ...errors import ParseError


def parse_syntax(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    network = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            raise ParseError("Format must be : <keyword>: <content>")

        keyword, content = line.split(":", 1)
        network.append((keyword.strip(), content.strip()))
    return network

# Output ideal:

# @dataclass
# class RawZone:
#     type: str
#     name: str
#     x: int
#     y: int
#     metadata: str | None