import pygame

from .camera import Camera
from .renderer import Renderer
from .screen import Screen
from ..state import State
from ...domain import Drone, Network


class Game:
    """Main controller for the simulation playback and visualization.

    This class orchestrates the full simulation lifecycle, including:
        - Pygame event handling
        - Time-based playback control
        - Camera management and viewport fitting
        - Rendering coordination
        - State extraction per timestep

    It acts as the central runtime loop that binds together the
    simulation model and the rendering system.
    """

    def __init__(
        self,
        network: Network,
        simulation: dict[Drone, list[State]],
    ):
        """Initialize the simulation game controller.

        Args:
            network: The underlying network graph of hubs and connections.
            simulation: Mapping from each drone to its timeline of states.
        """
        self.network = network
        self.simulation = simulation

        self.hubs = network.hubs
        self.connections = network.connections

        self.screen = Screen()

        self.info_panel_width = 300
        self.camera = Camera(
            self.screen.WIDTH - self.info_panel_width,
            self.screen.HEIGHT,
        )

        self.renderer = Renderer()

        self.current_timestep = 0

        self.max_timestep = max(
            state.timestep
            for states in simulation.values()
            for state in states
        )

        self.running = True

        self.playing = True

        self.step_delay_ms = 500

        self.last_step_time = (
            pygame.time.get_ticks()
        )

        self._fit_camera_to_graph()

    def run(self):
        """Run the main simulation loop until exit."""
        while self.running:

            self._handle_events()

            self._update_playback()

            self.screen.clear()

            current_states = (
                self._states_for_timestep(
                    self.current_timestep
                )
            )

            self.renderer.render(
                self.screen.surface,
                self.camera,
                self.network,
                current_states,
                self.current_timestep,
                self.max_timestep,
                self.playing,
                self.info_panel_width
            )

            self.screen.update()

        pygame.quit()

    def _update_playback(self):
        """Advance simulation time if playback is active."""

        if not self.playing:
            return

        now = pygame.time.get_ticks()

        if (
            now - self.last_step_time
            >= self.step_delay_ms
        ):

            self.last_step_time = now

            if (
                self.current_timestep
                < self.max_timestep
            ):
                self.current_timestep += 1

    def _handle_events(self):
        """Process user input events (keyboard and window events)."""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:

                    self.current_timestep = min(
                        self.max_timestep,
                        self.current_timestep + 1,
                    )

                elif event.key == pygame.K_LEFT:

                    self.current_timestep = max(
                        0,
                        self.current_timestep - 1,
                    )

                elif event.key == pygame.K_SPACE:

                    self.playing = (
                        not self.playing
                    )

                elif event.key == pygame.K_q:

                    self.camera.set_zoom(
                        self.camera.zoom * 1.1
                    )

                elif event.key == pygame.K_e:

                    self.camera.set_zoom(
                        self.camera.zoom / 1.1
                    )

    def _states_for_timestep(
        self,
        timestep,
    ):
        """Extract latest known state of each drone at a given timestep.

        Args:
            timestep: Simulation time to evaluate.

        Returns:
            Mapping from drones to their most recent state up to that time.
        """
        result = {}

        for drone, states in (
            self.simulation.items()
        ):

            valid = [
                state
                for state in states
                if state.timestep <= timestep
            ]

            if valid:
                result[drone] = valid[-1]

        return result

    def _fit_camera_to_graph(self):
        """Automatically center and scale camera to fit the network graph.

        Computes the bounding box of all hubs and adjusts:
            - camera center
            - zoom level

        This ensures the entire graph is visible within the viewport.
        """

        if not self.hubs:
            return

        xs = [
            hub.position[0]
            for hub in self.hubs
        ]

        ys = [
            hub.position[1]
            for hub in self.hubs
        ]

        min_x = min(xs)
        max_x = max(xs)

        min_y = min(ys)
        max_y = max(ys)

        center_x = (
            min_x + max_x
        ) / 2

        center_y = (
            min_y + max_y
        ) / 2

        self.camera.set_center(
            center_x,
            center_y,
        )

        graph_width = max(
            max_x - min_x,
            1,
        )

        graph_height = max(
            max_y - min_y,
            1,
        )

        viewport_width = (
            self.screen.WIDTH
            - self.info_panel_width
        )

        viewport_height = (
            self.screen.HEIGHT
        )

        #
        # margen alrededor del grafo
        #
        margin_factor = 0.90

        zoom_x = (
            viewport_width
            * margin_factor
            / graph_width
        )

        zoom_y = (
            viewport_height
            * margin_factor
            / graph_height
        )

        self.camera.set_zoom(
            min(
                zoom_x,
                zoom_y,
            )
        )
