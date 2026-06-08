import pygame


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
    WIDTH = 1600
    HEIGHT = 900
    FPS = 60

    def __init__(self):
        """Initialize the Pygame environment and create the display window."""
        pygame.init()

        self.surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "Drone Simulation"
        )

        self.clock = pygame.time.Clock()

    def clear(self):
        """Clear the screen by filling it with a white background."""
        self.surface.fill((255, 255, 255))

    def update(self):
        """Update the display and enforce the target FPS."""
        pygame.display.flip()
        self.clock.tick(self.FPS)
