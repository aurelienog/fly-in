from ...errors import InvalidSyntaxError
from .. import RawConnection
from ...utils import extract_metadata


def parse_connection(content: str) -> RawConnection:
    line, metadata = extract_metadata(content)

    if "-" not in content:
        raise InvalidSyntaxError("Connection must contain '-'")

    left, right = line.split("-", 1)

    a = left.strip()
    b = right.strip()

    if not a:
        raise InvalidSyntaxError("Invalid hub a")

    if not b:
        raise InvalidSyntaxError("Invalid hub b")

    return RawConnection(a, b, metadata)
