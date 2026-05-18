from ...errors import InvalidSyntaxError


def extract_metadata(line: str) -> tuple[str, str | None]:
    metadata = None

    has_open = "[" in line
    has_close = "]" in line

    if has_open != has_close:
        raise InvalidSyntaxError("Unclosed metadata block")

    if has_open:
        if line.count("[") != 1 or line.count("]") != 1:
            raise InvalidSyntaxError("Invalid metadata syntax")

        if line.index("[") > line.index("]"):
            raise InvalidSyntaxError("Invalid metadata syntax")

        line, metadata = line.split("[", 1)

        metadata = metadata.strip()

        if not metadata.endswith("]"):
            raise InvalidSyntaxError("Invalid metadata syntax")

        metadata = metadata[:-1].strip()

    return line.strip(), metadata


def parse_metadata(metadata: str | None) -> dict[str, str]:
    if metadata is None:
        return {}

    meta: dict[str, str] = {}

    for item in metadata.split():

        if "=" not in item:
            raise InvalidSyntaxError(f"invalid metadata item: {item}")

        key, value = item.split("=", 1)

        if not key or not value:
            raise InvalidSyntaxError(
                f"invalid metadata pair: {item}"
            )

        if key in meta:
            raise InvalidSyntaxError(
                f"duplicate metadata key: {key}"
            )

        meta[key] = value

    return meta
