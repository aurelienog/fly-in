from ...errors import InvalidSyntaxError


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
