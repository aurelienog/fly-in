from ...errors import InvalidSyntaxError
from .. import RawConnection


def parse_connection(content: str) -> RawConnection:
    if "-" not in content:
        raise InvalidSyntaxError("Connection must contain '-'")

    left, right = content.split("-", 1)

    hub1 = left.strip()
    if not hub1:
        raise InvalidSyntaxError("Invalid hub1")

    right = right.strip()

    metadata = None

    if "[" in right:
        if not right.endswith("]"):
            raise InvalidSyntaxError("Metadata must end with ]")

        hub2_part, metadata_part = right.split("[", 1)

        hub2 = hub2_part.strip()

        metadata = metadata_part.strip()

        if not metadata.endswith("]"):
            raise InvalidSyntaxError("Invalid metadata format")

        metadata = "[" + metadata

    else:
        hub2 = right

    if not hub2:
        raise InvalidSyntaxError("Invalid hub2")

    connection = RawConnection(hub1, hub2, metadata)
    return (connection)

# @dataclass
# class RawConnection:
#     a: str
#     b: str
#     metadata: str | None
