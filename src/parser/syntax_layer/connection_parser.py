from ...errors import InvalidSyntaxError
from ..models import RawConnection
from .metadata_parser import parse_metadata, extract_metadata


def parse_connection(
    content: str,
    line_doc: int
) -> RawConnection:

    ALLOWED_CONNECTION_METADATA = {
        "max_link_capacity",
    }

    line, metadata = extract_metadata(content)

    meta = parse_metadata(metadata)

    unknown = (set(meta) - ALLOWED_CONNECTION_METADATA)

    if unknown:
        raise InvalidSyntaxError(
            f"line {line_doc}: unknown metadata keys: {unknown}"
        )

    if "-" not in line:
        raise InvalidSyntaxError(
            f"line {line_doc}:connection must contain '-'"
        )

    left, right = line.split("-", 1)

    a = left.strip()
    b = right.strip()

    if not a:
        raise InvalidSyntaxError(
            f"line {line_doc}: invalid hub a"
        )

    if not b:
        raise InvalidSyntaxError(
            f"line {line_doc}: invalid hub b"
        )

    if "-" in a or "-" in b:
        raise InvalidSyntaxError(f"line {line_doc}: hub names cannot contain '-'")

    try:

        max_link_capacity = int(
            meta.get(
                "max_link_capacity",
                "1",
            )
        )

    except ValueError:

        raise InvalidSyntaxError(
            f"line {line_doc}: max_link_capacity must be integer"
        )

    return RawConnection(
        line=line_doc,
        a=a,
        b=b,
        max_link_capacity=max_link_capacity,
    )
