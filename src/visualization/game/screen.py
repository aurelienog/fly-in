import pygame


class Screen:
    WIDTH = 1600
    HEIGHT = 900
    FPS = 60

    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "Drone Simulation"
        )

        self.clock = pygame.time.Clock()

    def clear(self):
        self.surface.fill((255, 255, 255))

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
