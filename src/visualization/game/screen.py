try:
    import pygame
except ModuleNotFoundError:
    print(
        "\033[31m[ERROR] pygame is required to run this application.\n"
        "Please install it by running:\n"
        "    make\n"
        "or:\n"
        "    python -m pip install pygame\033[0m"
    )
    raise SystemExit(1)


class Screen:
    """Encapsulates the Pygame window and display loop utilities.

    This class is responsible for initializing and managing the main
    rendering surface, window configuration, and frame timing.

    It provides a minimal abstraction over Pygame's display system,
    including:

        - Window creation and configuration
        - Frame clearing
        - Frame buffer swapping
        - FPS control

    It is intended to be used as the base rendering surface for the
    simulation and renderer system.
    """
    WIDTH = 3600
    HEIGHT = 1800
    FPS = 60

    def __init__(self) -> None:
        """Initialize the Pygame environment and create the display window."""
        pygame.init()

        self.surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "Drone Simulation"
        )

        self.clock = pygame.time.Clock()

    def clear(self) -> None:
        """Clear the screen by filling it with a white background."""
        self.surface.fill((255, 255, 255))

    def update(self) -> None:
        """Update the display and enforce the target FPS."""
        pygame.display.flip()
        self.clock.tick(self.FPS)
