#!/usr/bin/env python3

from src.app import run_app
from src.errors import ParseError
import sys


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: ./fly_in <map_file>")
        sys.exit(1)

    try:
        run_app(sys.argv[1])
    except ParseError as exc:
        print(f"\033[31m[PARSE ERROR] {exc} \033[0m")
        sys.exit(1)

    except UnicodeError as exc:
        print(f"\033[31m[ERROR] invalid file encoding: {exc}\033[0m")
        sys.exit(1)

    except FileNotFoundError:
        print("\033[31m[ERROR] file not found\033[0m")
        sys.exit(1)

    except PermissionError:
        print("\033[31m[ERROR] access denied\033[0m")
        sys.exit(1)

    except OSError as exc:
        print("\033[31m[ERROR] system error:\033[0m", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
