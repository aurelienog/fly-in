import pygame
from ...domain import Drone, Hub, Connection, Color
from ...solver import SpaceTimeState
from .camera import Camera
from ..colors import RenderColors
from ..state import HubState, ConnectionState

from collections import deque


class PygameRenderer:
    """Renderiza los estados de los drones en una pantalla pygame."""

    def __init__(self):
        self.hub_radius = 15
        self.drone_radius = 8
        self.drone_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 20)

    def draw(
        self,
        start: Hub,
        screen: pygame.Surface,
        states: dict[Drone, SpaceTimeState],
        camera: Camera,
    ):
        """
        Dibuja todos los estados en la pantalla.

        Args:
            screen: superficie de pygame
            states: {drone: SpaceTimeState} con los estados actuales
            camera: cámara para transformación de coordenadas
        """
        self._draw_network(start, screen, camera)

        # for drone, state in states.items():
        #     position = camera.world_to_screen(
        #         state.hub.position[0],
        #         state.hub.position[1]
        #     )
        #     self._draw_drones(drone, position, screen.surface)
        for drone, state in states.items():

            if isinstance(state, HubState):

                position = camera.world_to_screen(
                    *state.hub.position
                )

            elif isinstance(state, ConnectionState):

                x1, y1 = state.from_hub.position
                x2, y2 = state.to_hub.position

                world_x = (
                    x1
                    +
                    (x2 - x1) * state.progress
                )

                world_y = (
                    y1
                    +
                    (y2 - y1) * state.progress
                )

                position = camera.world_to_screen(
                    world_x,
                    world_y
                )

            self._draw_drones(
                drone,
                position,
                screen.surface
            )


    def draw_text(
        self,
        screen: pygame.Surface,
        text: str,
        pos: tuple[int, int],
        color: tuple[int, int, int] = (0, 0, 0),
        font_size: int = 24,
    ):
        """Dibuja texto en la pantalla."""
        font = pygame.font.Font(None, font_size)
        surface = font.render(text, True, color)
        screen.blit(surface, pos)

    def _draw_network(self, start: Hub, screen, camera):
        queue = deque([start])
        visited = {start}

        while queue:
            current = queue.popleft()

            self._draw_hub(current, screen.surface, camera)

            for connection in current.connections:
                neighbor = connection.get_neighbor(current)

                self._draw_connection(connection, screen.surface, camera)

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def _draw_hub(self, hub: Hub, surface, camera):
        position = camera.world_to_screen(*hub.position)
        if hub.color == Color.RAINBOW:
            color = RenderColors.rainbow_color_at(*hub.position)
        else:
            color = RenderColors.PYGAME[hub.color]
        print(
            hub.name,
            hub.position,
            camera.world_to_screen(*hub.position)
        )
        pygame.draw.circle(
            surface,
            color,
            position,
            self.hub_radius,
        )

    def _draw_connection(self, connection: Connection, surface, camera):
        start = camera.world_to_screen(*connection.hubs[0].position)
        end = camera.world_to_screen(*connection.hubs[1].position)

        pygame.draw.line(
            surface,
            (100, 100, 100),
            start,
            end,
            2,
        )

    def _draw_drones(self, drone, position, surface):

        pygame.draw.circle(
            surface,
            self.drone_color,
            position,
            self.drone_radius
        )

        text = self.font.render(
            str(drone.id),
            True,
            (0, 0, 0)
        )

        text_rect = text.get_rect(
            center=(
                position[0],
                position[1] - self.drone_radius - 12
            )
        )

        surface.blit(text, text_rect)