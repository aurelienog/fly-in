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
    line_doc: int,
    nb_drones: int
) -> RawHub:
    """Parse a hub definition from a raw text line.

    The function extracts hub coordinates, name, type, and optional
    metadata such as zone, color, and maximum number of drones.

    Args:
        content: Raw hub definition string.
        hub_type: Type of hub (e.g., start, end, or regular hub).
        line_doc: Line number in the source file for error reporting.

    Returns:
        The parsed raw hub representation.

    Raises:
        InvalidSyntaxError: If the hub definition has invalid syntax,
            contains unknown metadata keys, uses invalid coordinates,
            or includes malformed numeric values.
    """

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

    except ValueError:
        raise InvalidSyntaxError(
            f"line {line_doc}: x, y and max_drones must be integers"
        )

    value = meta.get("max_drones")

    if value is None:
        max_drones = None
    else:
        try:
            max_drones = int(value)
        except ValueError:
            raise InvalidSyntaxError(
                f"line {line_doc}: max_drones must be an integer"
            )

    if hub_type == "start_hub" and max_drones is None:
        max_drones = nb_drones

    if hub_type == "end_hub" and max_drones is None:
        max_drones = nb_drones

    if max_drones is None:
        max_drones = 1

    return RawHub(
        line=line_doc,
        hub_type=hub_type,
        name=name,
        x=x_int,
        y=y_int,

        zone=meta.get("zone", "normal"),
        color=meta.get("color", "default"),
        max_drones=max_drones,
    )
