import math
import random

from core.constants import *

class Projectile:

    def __init__(
        self,
        x,
        y,
        angle,
        tilemap
    ):

        self.tilemap = tilemap

        self.x = x
        self.y = y

        self.angle = angle

        radians = math.radians(angle)

        self.vx = math.cos(radians)
        self.vy = math.sin(radians)

        self.speed = 140

        self.distance_travelled = 0
        self.max_distance = TILE_SIZE * 16

        self.dead = False

        self.smoke_timer = 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        old_x = self.x
        old_y = self.y

        move_x = self.vx * self.speed * dt
        move_y = self.vy * self.speed * dt

        self.x += move_x
        self.y += move_y

        distance = math.sqrt(
            move_x * move_x +
            move_y * move_y
        )

        self.distance_travelled += distance

        # =================================================
        # RANGE LIMIT
        # =================================================

        if self.distance_travelled >= self.max_distance:

            self.create_impact()

            self.dead = True

            return

        # =================================================
        # MAP BOUNDS
        # =================================================

        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        terrain = self.tilemap.get_tile(
            tile_x,
            tile_y
        )

        if terrain is None:

            self.dead = True

            return

        # =================================================
        # FOREST INTERCEPTION
        # =================================================

        if terrain == TERRAIN_FOREST:

            if random.random() < 0.15:

                self.create_impact()

                self.dead = True

                return

    # =====================================================
    # IMPACT
    # =====================================================

    def create_impact(self):

        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        self.tilemap.add_ground_damage(
            tile_x,
            tile_y,
            0.18
        )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        surface.fill(
            (255, 240, 180),
            (int(screen_x), int(screen_y), 2, 2)
        )