import random

from core.constants import *

class SmokeParticle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.life = random.uniform(0.4, 0.8)

        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -2)

    def update(self, dt):

        self.life -= dt

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface, camera):

        screen_x, screen_y = camera.apply(self.x, self.y)

        surface.fill(
            EXHAUST,
            (int(screen_x), int(screen_y), 1, 1)
        )

    @property
    def dead(self):

        return self.life <= 0