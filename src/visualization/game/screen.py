import pygame


class Screen:
    """Gestiona la ventana de pygame."""

    WIDTH = 1280
    HEIGHT = 720
    FPS = 60

    def __init__(self, title: str = "Fly-in Visualization"):
        pygame.init()
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def update(self):
        """Actualiza la pantalla."""
        pygame.display.flip()

    def tick(self, fps: int = FPS):
        """Controla FPS."""
        self.clock.tick(fps)

    def fill(self, color: tuple[int, int, int] = (255, 255, 255)):
        """Limpia la pantalla con un color."""
        self.surface.fill(color)

    def quit(self):
        """Cierra pygame."""
        pygame.quit()
