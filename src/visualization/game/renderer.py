import pygame
from collections import defaultdict

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
        max_timestep,
        playing,
        info_panel_width
    ):
        self._draw_connections(screen, camera, network.connections)
        self._draw_hubs(screen, camera, network.hubs)
        self._draw_drones(screen, camera, drone_states)
        self._draw_timestep(screen, timestep)
        self._draw_info(screen, network, drone_states, timestep, max_timestep, playing, info_panel_width)

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
            color = hub.color

            if color == Color.RAINBOW:
                pygame_color = (RenderColors.PYGAME[Color.INDIGO])
            else:
                pygame_color = RenderColors.PYGAME[hub.color]
            pygame.draw.circle(
                screen,
                pygame_color,
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

    def _draw_info(
        self,
        screen,
        network,
        drone_states,
        timestep,
        max_timestep,
        playing,
        info_panel_width
    ):
        panel_x = (
            screen.get_width()
            - info_panel_width
        )

        pygame.draw.rect(
            screen,
            (245, 245, 245),
            (
                panel_x,
                0,
                info_panel_width,
                screen.get_height(),
            ),
        )

        pygame.draw.line(
            screen,
            (180, 180, 180),
            (panel_x, 0),
            (panel_x, screen.get_height()),
            2,
        )

        title_font = pygame.font.SysFont(
            None,
            32,
            bold=True,
        )

        font = pygame.font.SysFont(
            None,
            24,
        )

        small_font = pygame.font.SysFont(
            None,
            20,
        )

        y = 20

        title = title_font.render(
            "Drone Simulation",
            True,
            (0, 0, 0),
        )

        screen.blit(
            title,
            (panel_x + 15, y),
        )

        y += 50

        status = (
            "PLAYING"
            if playing
            else "PAUSED"
        )

        screen.blit(
            font.render(
                f"Status: {status}",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 35

        screen.blit(
            font.render(
                f"Timestep: {timestep}/{max_timestep}",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 50

        screen.blit(
            font.render(
                "Controls",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 30

        controls = [
            "SPACE : Play/Pause",
            "LEFT  : Previous",
            "RIGHT : Next",
            "Q     : Zoom In",
            "E     : Zoom Out",
        ]

        for text in controls:
            screen.blit(
                small_font.render(
                    text,
                    True,
                    (50, 50, 50),
                ),
                (panel_x + 20, y),
            )
            y += 22

        y += 20

        screen.blit(
            font.render(
                "Network",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 30

        network_stats = [
            f"Hubs: {len(network.hubs)}",
            f"Connections: {len(network.connections)}",
        ]

        for text in network_stats:
            screen.blit(
                small_font.render(
                    text,
                    True,
                    (50, 50, 50),
                ),
                (panel_x + 20, y),
            )
            y += 22

        y += 20

        hub_occ = defaultdict(int)
        conn_occ = defaultdict(int)

        for state in drone_states.values():

            if isinstance(state, HubState):
                hub_occ[state.hub] += 1

            elif isinstance(state, ConnectionState):
                conn_occ[state.connection] += 1

        active = len(drone_states)

        completed = 0

        for drone, state in drone_states.items():

            if (
                isinstance(state, HubState)
                and state.hub == network.end_hub
            ):
                completed += 1

        y += 10

        screen.blit(
            font.render(
                "Drones",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 30

        drone_stats = [
            f"Visible: {active}",
            f"Completed: {completed}",
        ]

        for text in drone_stats:
            screen.blit(
                small_font.render(
                    text,
                    True,
                    (50, 50, 50),
                ),
                (panel_x + 20, y),
            )
            y += 22

        y += 30

        screen.blit(
            font.render(
                "Legend",
                True,
                (0, 0, 0),
            ),
            (panel_x + 15, y),
        )

        y += 30

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (panel_x + 30, y),
            8,
        )

        screen.blit(
            small_font.render(
                "Drone",
                True,
                (0, 0, 0),
            ),
            (panel_x + 50, y - 8),
        )

        y += 30

        pygame.draw.circle(
            screen,
            (100, 150, 255),
            (panel_x + 30, y),
            10,
        )

        screen.blit(
            small_font.render(
                "Hub",
                True,
                (0, 0, 0),
            ),
            (panel_x + 50, y - 8),
        )

        y += 30

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (panel_x + 20, y),
            (panel_x + 40, y),
            3,
        )

        screen.blit(
            small_font.render(
                "Connection",
                True,
                (0, 0, 0),
            ),
            (panel_x + 50, y - 8),
        )