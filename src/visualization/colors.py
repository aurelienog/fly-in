from ..domain import Color


class RenderColors:

    RAINBOW_COLORS = [
        Color.RED,
        Color.ORANGE,
        Color.YELLOW,
        Color.GREEN,
        Color.BLUE,
        Color.INDIGO,
        Color.VIOLET,
    ]

    ANSI = {
        Color.RED: "\033[31m",
        Color.DARKRED: "\033[38;5;88m",
        Color.GREEN: "\033[32m",
        Color.YELLOW: "\033[33m",
        Color.BLUE: "\033[34m",
        Color.PURPLE: "\033[35m",
        Color.VIOLET: "\033[0;95m",
        Color.CYAN: "\033[36m",
        Color.WHITE: "\033[37m",
        Color.ORANGE: "\033[38;5;208m",
        Color.MAROON: "\033[38;5;52m",
        Color.BROWN: "\033[38;5;94m",
        Color.BLACK: "\033[90m",
        Color.CRIMSON: "\033[38;5;161m",
        Color.INDIGO: "\033[38;5;54m",
        Color.GOLD: "\033[38;5;220m",
        Color.DEFAULT: "\033[0m"
    }

    PYGAME = {
        Color.RED: (180, 40, 40),
        Color.DARKRED: (88, 0, 0),
        Color.GREEN: (40, 140, 40),
        Color.YELLOW: (180, 180, 40),
        Color.BLUE: (40, 80, 180),
        Color.PURPLE: (128, 0, 128),
        Color.VIOLET: (148, 0, 211),
        Color.CYAN: (0, 139, 139),
        Color.WHITE: (220, 220, 220),
        Color.ORANGE: (208, 120, 0),
        Color.MAROON: (80, 20, 20),
        Color.BROWN:  (139, 69, 19),
        Color.BLACK: (100, 100, 100),
        Color.CRIMSON: (161, 20, 60),
        Color.INDIGO: (54, 40, 120),
        Color.GOLD: (212, 175, 55),
        Color.DEFAULT: (40, 40, 40)
    }

    @classmethod
    def ANSI_rainbow(cls, text: str) -> str:
        return "".join(
            cls.ANSI[
                cls.RAINBOW_COLORS[i % len(cls.RAINBOW_COLORS)]
            ] + ch
            for i, ch in enumerate(text)
        ) + cls.ANSI[Color.DEFAULT]

    @classmethod
    def rainbow_color_at(cls, x: int, y: int):
        colors = [
            cls.PYGAME[Color.RED],
            cls.PYGAME[Color.ORANGE],
            cls.PYGAME[Color.YELLOW],
            cls.PYGAME[Color.GREEN],
            cls.PYGAME[Color.BLUE],
            cls.PYGAME[Color.INDIGO],
            cls.PYGAME[Color.VIOLET],
        ]

        return colors[(x + y) % len(colors)]
