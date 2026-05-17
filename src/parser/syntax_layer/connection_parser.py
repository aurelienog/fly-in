from ...errors import InvalidSyntaxError
from .. import RawConnection
from ...utils import extract_metadata
from . import parse_metadata

ALLOWED_CONNECTION_METADATA = {
    "max_link_capacity",
}


def parse_connection(
    content: str,
) -> RawConnection:

    line, metadata = extract_metadata(content)

    meta = parse_metadata(metadata)

    unknown = (set(meta) - ALLOWED_CONNECTION_METADATA)

    if unknown:
        raise InvalidSyntaxError(
            f"unknown metadata keys: {unknown}"
        )

    if "-" not in line:
        raise InvalidSyntaxError(
            "connection must contain '-'"
        )

    left, right = line.split("-", 1)

    a = left.strip()
    b = right.strip()

    if not a:
        raise InvalidSyntaxError(
            "invalid hub a"
        )

    if not b:
        raise InvalidSyntaxError(
            "invalid hub b"
        )

    try:

        max_link_capacity = int(
            meta.get(
                "max_link_capacity",
                "1",
            )
        )

    except ValueError:

        raise InvalidSyntaxError(
            "max_link_capacity must be integer"
        )

    return RawConnection(
        a=a,
        b=b,
        max_link_capacity=max_link_capacity,
    )
