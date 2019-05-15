from core.config import IMAGE_SEGMENT_SIZE_PX as WIDTH, IMAGE_SEGMENT_SIZE_PX as HEIGHT


class Detection:
    def __init__(self,
                 x: int,
                 y: int,
                 mass: float,
                 width: int = WIDTH,
                 height: int = HEIGHT):
        self.x = x
        self.y = y
        self.mass = mass
        self.width = width
        self.height = height
