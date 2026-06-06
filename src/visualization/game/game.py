from .timeline import Timeline
from .renderer import PygameRenderer
from .screen import Screen
from .camera import Camera
from ..state import HubState, ConnectionState


class Game:

    def __init__(self, solution):

        self.timeline = solution
        self.renderer = PygameRenderer()
        self.camera = Camera(1280, 720)
        self.screen = Screen()

        self.timestep = 0

        self.center_x, self.center_y = self.compute_map_center(
            solution
        )

    def run(self, start):

        import pygame

        clock = pygame.time.Clock()
        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        self.timestep = min(
                            self.timestep + 1,
                            self.timeline.max_timestep
                        )

                    elif event.key == pygame.K_LEFT:
                        self.timestep = max(self.timestep - 1, 0)

            self.screen.fill("white")

            self.camera.x = self.center_x
            self.camera.y = self.center_y

            states = self.timeline.states_at(self.timestep)

            self.renderer.draw(
                start,
                self.screen,
                states,
                self.camera
            )

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()

    def compute_map_center(self, solution):
        xs = []
        ys = []

        for states in solution.values():
            for state in states:

                if isinstance(state, HubState):
                    xs.append(state.hub.position[0])
                    ys.append(state.hub.position[1])

                elif isinstance(state, ConnectionState):
                    from_x, from_y = state.from_hub.position
                    to_x, to_y = state.to_hub.position

                    xs.extend([from_x, to_x])
                    ys.extend([from_y, to_y])

        if not xs:
            return 0, 0

        return (
            (min(xs) + max(xs)) / 2,
            (min(ys) + max(ys)) / 2,
        )
