from ...errors import InvalidSyntaxError


def parse_nb_drones(content: str) -> int:
    value = content.strip()

    if not value:
        raise InvalidSyntaxError("Missing drone count")

    try:
        return int(value)
    except ValueError:
        raise InvalidSyntaxError("Drone count must be an integer")
