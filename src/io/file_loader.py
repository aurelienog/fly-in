def read_file(file: str) -> str:
    with open(file, "r") as f:
        content = f.read()
    return content
