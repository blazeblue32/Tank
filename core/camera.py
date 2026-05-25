from core.constants import *

class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):

        self.x = target_x - (SCREEN_WIDTH // 2)
        self.y = target_y - (SCREEN_HEIGHT // 2)

    def apply(self, x, y):

        return (
            x - self.x,
            y - self.y
        )