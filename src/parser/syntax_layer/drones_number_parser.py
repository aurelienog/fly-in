from ...errors import InvalidSyntaxError


def parse_nb_drones(content: str, line: int) -> int:
    value = content.strip()

    if not value:
        raise InvalidSyntaxError(f"line {line}: Missing drone count")

    try:
        return int(value)
    except ValueError:
        raise InvalidSyntaxError(f"line {line}: Drone count must be an integer")
