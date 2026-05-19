from ...errors import InvalidSyntaxError
from ..models import RawHub
from .metadata_parser import parse_metadata, extract_metadata


ALLOWED_HUB_METADATA = {
    "zone",
    "color",
    "max_drones",
}


def parse_hub(
    content: str,
    hub_type: str,
    line_doc: int
) -> RawHub:

    line, metadata = extract_metadata(content)

    meta = parse_metadata(metadata)

    unknown = set(meta) - ALLOWED_HUB_METADATA
    if unknown:
        raise InvalidSyntaxError(
            f"line {line_doc} unknown metadata keys: {unknown}"
        )

    parts = line.split()

    if len(parts) != 3:
        raise InvalidSyntaxError(
            f"line {line_doc}: invalid hub syntax"
        )

    name, x, y = parts

    if "-" in name:
        raise InvalidSyntaxError(f"line {line_doc}: hub names cannot contain '-'")

    try:
        x_int = int(x)
        y_int = int(y)

        max_drones = int(
            meta.get("max_drones", "1")
        )

    except ValueError:
        raise InvalidSyntaxError(
            f"line {line_doc}: x, y and max_drones must be integers"
        )

    return RawHub(
        line=line_doc,
        hub_type=hub_type,
        name=name,
        x=x_int,
        y=y_int,

        zone=meta.get("zone", "normal"),
        color=meta.get("color"),
        max_drones=max_drones,
    )
