from ...errors import InvalidSyntaxError


def parse_nb_drones(content: str, line: int) -> int:
    """Parse the number of drones from a raw text value.

    Args:
        content: Raw string containing the drone count.
        line: Line number in the source file for error reporting.

    Returns:
        The number of drones as an integer.

    Raises:
        InvalidSyntaxError: If the value is missing or cannot be parsed
            as a valid integer.
    """
    value = content.strip()

    if not value:
        raise InvalidSyntaxError(f"line {line}: Missing drone count")

    try:
        return int(value)
    except ValueError:
        raise InvalidSyntaxError(f"line {line}: Drone count must be an integer")
