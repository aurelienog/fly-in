class Camera:
    """Represents a 2D camera that maps world coordinates to screen space.

    The camera is responsible for transforming simulation/world coordinates
    into screen coordinates for rendering. It supports translation (center
    position) and scaling (zoom level).

    This class is typically used by rendering systems to visualize a
    graph-based or spatial simulation.
    """

    def __init__(self, viewport_width: int, viewport_height: int) -> None:
        """Initialize the camera with a viewport size.

        Args:
            viewport_width: Width of the rendering viewport in pixels.
            viewport_height: Height of the rendering viewport in pixels.
        """
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.x: float = 0.0
        self.y: float = 0.0

        self.zoom = 50.0

    def world_to_screen(
        self,
        world_x: float,
        world_y: float,
    ) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates.

        Applies translation (camera position) and scaling (zoom level)
        to map simulation space into pixel space.

        Args:
            world_x: X coordinate in world space.
            world_y: Y coordinate in world space.

        Returns:
            A tuple (x, y) representing pixel coordinates on screen.
        """

        screen_x = (
            (world_x - self.x) * self.zoom
            + self.viewport_width / 2
        )

        screen_y = (
            (world_y - self.y) * self.zoom
            + self.viewport_height / 2
        )

        return int(screen_x), int(screen_y)

    def set_center(
        self,
        x: float,
        y: float,
    ) -> None:
        """Set the world-space position of the camera center.

        Args:
            x: X coordinate of the new camera center.
            y: Y coordinate of the new camera center.
        """
        self.x = x
        self.y = y

    def set_zoom(
        self,
        zoom: float,
    ) -> None:
        """Set the camera zoom level.

        Args:
            zoom: Zoom factor. Must be greater than 0.
        """
        if zoom > 0:
            self.zoom = zoom
