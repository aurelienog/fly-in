from ...errors import InvalidSyntaxError


def parse_nb_drones(content: str) -> None:
    try:
        value = int(content.strip())
    except ValueError:
        raise InvalidSyntaxError("nb_drone must be an integer")

    if value < 0:
        raise InvalidSyntaxError("nb_drone must be >= 0")
