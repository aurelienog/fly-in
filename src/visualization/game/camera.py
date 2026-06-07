class Camera:
    """Transforma coordenadas del mundo a coordenadas de pantalla."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.x = 0
        self.y = 0

        self.zoom = 50.0

    def world_to_screen(
        self,
        world_x: float,
        world_y: float,
    ) -> tuple[int, int]:

        screen_x = (
            (world_x - self.x) * self.zoom
            + self.width / 2
        )

        screen_y = (
            (world_y - self.y) * self.zoom
            + self.height / 2
        )

        return int(screen_x), int(screen_y)

    def set_center(
        self,
        x: float,
        y: float,
    ):
        self.x = x
        self.y = y

    def set_zoom(
        self,
        zoom: float,
    ):
        if zoom > 0:
            self.zoom = zoom

    def _fit_camera_to_graph(self):

        if not self.network.hubs:
            return

        xs = [
            hub.position[0]
            for hub in self.network.hubs
        ]

        ys = [
            hub.position[1]
            for hub in self.network.hubs
        ]

        min_x = min(xs)
        max_x = max(xs)

        min_y = min(ys)
        max_y = max(ys)

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

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

        margin = 0.75

        zoom_x = (
            self.screen.WIDTH
            * margin
            / graph_width
        )

        zoom_y = (
            self.screen.HEIGHT
            * margin
            / graph_height
        )

        self.camera.set_zoom(
            min(
                zoom_x,
                zoom_y,
            )
        )
