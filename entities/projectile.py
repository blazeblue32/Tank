import math
import random

from core.constants import *

from entities.particle import (
    ImpactParticle,
    ImpactFlash
)

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

        # =================================================
        # MOVEMENT
        # =================================================

        self.speed = 140

        self.distance_travelled = 0

        range_roll = random.random()

        if range_roll < 0.25:

            shell_range = 16

        elif range_roll < 0.75:

            shell_range = 17

        else:

            shell_range = 18

        self.max_distance = (
            TILE_SIZE * shell_range
        )

        # =================================================
        # OBSTRUCTION
        # =================================================

        self.obstruction = 0

        # =================================================
        # EFFECTS
        # =================================================

        self.impact_particles = []

        self.impact_flashes = []

        # =================================================
        # STATE
        # =================================================

        self.dead = False

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        # =================================================
        # EFFECTS
        # =================================================

        for particle in self.impact_particles:
            particle.update(dt)

        self.impact_particles = [
            p for p in self.impact_particles
            if not p.dead
        ]

        for flash in self.impact_flashes:
            flash.update(dt)

        self.impact_flashes = [
            f for f in self.impact_flashes
            if not f.dead
        ]

        if self.dead:
            return

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
        # CONCEALMENT
        # =================================================

        concealment_density = 0

        if terrain == TERRAIN_FOREST:

            concealment_density = 2.0

        # =================================================
        # OBSTRUCTION
        # =================================================

        if concealment_density > 0:

            range_factor = (
                self.distance_travelled /
                self.max_distance
            )

            range_factor = max(
                0.15,
                range_factor
            )

            self.obstruction += (
                concealment_density *
                range_factor *
                dt
            )

            intercept_probability = (
                1 - math.exp(
                    -self.obstruction
                )
            )

            if random.random() < intercept_probability:

                self.create_impact()

                self.dead = True

                return

    # =====================================================
    # IMPACT
    # =====================================================

    def create_impact(self):

        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        terrain = self.tilemap.get_tile(
            tile_x,
            tile_y
        )

        # =================================================
        # RADIAL TERRAIN DAMAGE
        # =================================================

        self.tilemap.add_radial_ground_damage(
            tile_x,
            tile_y,
            radius=1,
            center_damage=0.18
        )
        
        # =================================================
        # CRATER MARK
        # =================================================

        if terrain != TERRAIN_WATER:

            self.tilemap.add_crater_mark(
                tile_x,
                tile_y,
                2,
                4
            )

        # =================================================
        # FLASH
        # =================================================

        self.impact_flashes.append(
            ImpactFlash(
                self.x,
                self.y
            )
        )

        # =================================================
        # DIRT
        # =================================================

        for _ in range(10):

            self.impact_particles.append(
                ImpactParticle(
                    self.x,
                    self.y,
                    (80, 70, 60),
                    0.30,
                    50
                )
            )

        # =================================================
        # SPARKS
        # =================================================

        for _ in range(4):

            self.impact_particles.append(
                ImpactParticle(
                    self.x,
                    self.y,
                    (255, 220, 120),
                    0.12,
                    80
                )
            )

        # =================================================
        # SMOKE
        # =================================================

        for _ in range(5):

            self.impact_particles.append(
                ImpactParticle(
                    self.x,
                    self.y,
                    (120, 120, 120),
                    0.45,
                    30
                )
            )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        # =================================================
        # FLASHES
        # =================================================

        for flash in self.impact_flashes:
            flash.draw(surface, camera)

        # =================================================
        # PARTICLES
        # =================================================

        for particle in self.impact_particles:
            particle.draw(surface, camera)

        if self.dead:
            return

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        # =================================================
        # SHELL
        # =================================================

        surface.fill(
            (255, 240, 180),
            (
                int(screen_x),
                int(screen_y),
                2,
                2
            )
        )

        # =================================================
        # TRAIL
        # =================================================

        trail_x = screen_x - (self.vx * 2)
        trail_y = screen_y - (self.vy * 2)

        surface.fill(
            (180, 180, 180),
            (
                int(trail_x),
                int(trail_y),
                1,
                1
            )
        )