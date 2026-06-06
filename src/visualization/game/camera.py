class Camera:
    """Transforma coordenadas del mundo a coordenadas de pantalla."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = 0  # Centro del mundo en X
        self.y = 0  # Centro del mundo en Y
        self.zoom = 50.0  # 1.0 = escala normal

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[int, int]:
        """
        Convierte coordenadas del mundo a coordenadas de pantalla.
        Args:
            world_x, world_y: coordenadas en el mundo
        Returns:
            (screen_x, screen_y): coordenadas en la pantalla
        """
        screen_x = (world_x - self.x) * self.zoom + self.width / 2
        screen_y = (world_y - self.y) * self.zoom + self.height / 2
        return int(screen_x), int(screen_y)

    def set_center(self, x: float, y: float):
        """Centra la cámara en un punto del mundo."""
        self.x = x
        self.y = y

    def set_zoom(self, zoom: float):
        """Cambia el zoom de la cámara."""
        if zoom > 0:
            self.zoom = zoom
