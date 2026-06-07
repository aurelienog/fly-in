import pygame

from ..state import HubState, ConnectionState
from ..colors import RenderColors, Color


class Renderer:
    HUB_RADIUS = 22
    DRONE_RADIUS = 10

    def render(
        self,
        screen,
        camera,
        network,
        drone_states,
        timestep,
    ):
        self._draw_connections(screen, camera, network.connections)
        self._draw_hubs(screen, camera, network.hubs)
        self._draw_drones(screen, camera, drone_states)
        self._draw_timestep(screen, timestep)

    def _draw_connections(
        self,
        screen,
        camera,
        connections,
    ):
        for connection in connections:

            a, b = connection.hubs

            ax, ay = a.position
            bx, by = b.position

            p1 = camera.world_to_screen(
                ax,
                ay,
            )

            p2 = camera.world_to_screen(
                bx,
                by,
            )

            pygame.draw.line(
                screen,
                RenderColors.PYGAME[Color.BLACK],
                p1,
                p2,
                3,
            )

    def _draw_hubs(
        self,
        screen,
        camera,
        hubs,
    ):
        font = pygame.font.SysFont(
            None,
            22,
        )

        for hub in hubs:

            x, y = hub.position

            pos = camera.world_to_screen(
                x,
                y,
            )

            pygame.draw.circle(
                screen,
                RenderColors.PYGAME[hub.color],
                pos,
                self.HUB_RADIUS,
            )

            text = font.render(
                hub.name,
                True,
                RenderColors.PYGAME[Color.BLACK],
            )

            screen.blit(
                text,
                (
                    pos[0] - 20,
                    pos[1] - 40,
                ),
            )

    def _draw_drones(
        self,
        screen,
        camera,
        drone_states,
    ):
        font = pygame.font.SysFont(
            None,
            18,
        )

        for drone, state in drone_states.items():

            x, y = self._state_position(
                state,
            )

            screen_pos = camera.world_to_screen(
                x,
                y,
            )

            pygame.draw.circle(
                screen,
                (0, 0, 0),
                screen_pos,
                self.DRONE_RADIUS,
            )

            label = font.render(
                drone.id,
                True,
                (255, 255, 255),
            )

            screen.blit(
                label,
                (
                    screen_pos[0] - 8,
                    screen_pos[1] - 5,
                ),
            )

    def _draw_timestep(
        self,
        screen,
        timestep,
    ):
        font = pygame.font.SysFont(
            None,
            40,
        )

        text = font.render(
            f"Timestep: {timestep}",
            True,
            (255, 255, 255),
        )

        screen.blit(
            text,
            (20, 20),
        )

    def _state_position(
        self,
        state,
    ):
        if isinstance(
            state,
            HubState,
        ):
            return state.hub.position

        if isinstance(
            state,
            ConnectionState,
        ):
            sx, sy = state.from_hub.position
            ex, ey = state.to_hub.position

            x = sx + (ex - sx) * state.progress
            y = sy + (ey - sy) * state.progress

            return x, y

        raise ValueError(
            f"Unknown state type: {type(state)}"
        )
