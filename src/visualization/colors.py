class ColorPalette:
    RESET = "\033[0m"

    # foreground
    RED = "\033[31m"
    DARKRED = "\033[38;5;88m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    VIOLET = "\033[0;95m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    ORANGE = "\033[38;5;208m"
    MAROON = "\033[38;5;52m"
    GRAY = "\033[90m"
    CRIMSON = "\033[38;5;161m"
    INDIGO = "\033[38;5;54m"

    # background
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    COLORS = [
        RED,
        DARKRED,
        GREEN,
        YELLOW,
        BLUE,
        PURPLE,
        CYAN,
        WHITE,
        GRAY,
        ORANGE,
        MAROON,
        CRIMSON,
        INDIGO
        ]

    BACKGROUNDS = [
            BG_GREEN,
            BG_YELLOW,
            BG_BLUE,
            BG_PURPLE,
            BG_CYAN,
            BG_WHITE,
            BG_RED,
        ]

    RAINBOW_COLORS = [
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        BLUE,
        INDIGO,
        VIOLET,
    ]

    @classmethod
    def rainbow(cls, text: str) -> str:
        return "".join(
            cls.RAINBOW_COLORS[i % len(cls.RAINBOW_COLORS)] + ch
            for i, ch in enumerate(text)
        ) + ColorPalette.RESET
