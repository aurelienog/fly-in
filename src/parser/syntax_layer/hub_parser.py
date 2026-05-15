from ...errors import InvalidSyntaxError
from ..models import RawHub
from ...utils import extract_metadata


def parse_hub(content: str, hub_type: str) -> RawHub:
    line, metadata = extract_metadata(content)

    parts = line.split()

    if len(parts) != 3:
        raise InvalidSyntaxError("Invalid hub syntax")

    name, x, y = parts

    return RawHub(hub_type, name, x, y, metadata)
