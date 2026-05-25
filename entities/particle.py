import random
import math
import pygame

from core.constants import *

# =========================================================
# SMOKE PARTICLE
# =========================================================

class SmokeParticle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.life = random.uniform(0.12, 2.4)

        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -2)

    def update(self, dt):

        self.life -= dt

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface, camera):

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        surface.fill(
            EXHAUST,
            (
                int(screen_x),
                int(screen_y),
                1,
                1
            )
        )

    @property
    def dead(self):

        return self.life <= 0

# =========================================================
# IMPACT PARTICLE
# =========================================================

class ImpactParticle:

    def __init__(
        self,
        x,
        y,
        color,
        lifetime,
        speed
    ):

        self.x = x
        self.y = y

        self.color = color

        self.life = lifetime

        angle = random.uniform(0, math.pi * 2)

        velocity = random.uniform(
            speed * 0.5,
            speed
        )

        self.vx = math.cos(angle) * velocity
        self.vy = math.sin(angle) * velocity

    def update(self, dt):

        self.life -= dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vx *= 0.90
        self.vy *= 0.90

    def draw(self, surface, camera):

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        surface.fill(
            self.color,
            (
                int(screen_x),
                int(screen_y),
                1,
                1
            )
        )

    @property
    def dead(self):

        return self.life <= 0

# =========================================================
# IMPACT FLASH
# =========================================================

class ImpactFlash:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.life = 0.08

        self.max_radius = 5

    def update(self, dt):

        self.life -= dt

    def draw(self, surface, camera):

        if self.life <= 0:
            return

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        progress = self.life / 0.08

        radius = int(
            self.max_radius * progress
        )

        pygame.draw.circle(
            surface,
            (255, 240, 180),
            (
                int(screen_x),
                int(screen_y)
            ),
            max(1, radius),
            1
        )

    @property
    def dead(self):

        return self.life <= 0