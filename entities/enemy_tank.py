import pygame
import math

from core.constants import *
from entities.tank_base import TankBase

class EnemyTank(TankBase):

    def __init__(
        self,
        tilemap,
        x,
        y
    ):

        super().__init__(tilemap)

        self.x = x
        self.y = y

        self.tile_x = x // TILE_SIZE
        self.tile_y = y // TILE_SIZE

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        pass

    # =====================================================
    # ARMOR CHECK
    # =====================================================

    def get_hit_armor(
        self,
        projectile_angle
    ):

        angle_to_front = {

            NORTH: 270,
            EAST: 0,
            SOUTH: 90,
            WEST: 180,
        }

        front_angle = angle_to_front[
            self.hull_facing
        ]

        relative = (
            projectile_angle -
            front_angle
        ) % 360

        # ================================================
        # FRONT
        # ================================================

        if (
            relative <= 30 or
            relative >= 330
        ):

            return self.front_armor, "FRONT"

        # ================================================
        # REAR
        # ================================================

        if (
            150 <= relative <= 210
        ):

            return self.rear_armor, "REAR"

        # ================================================
        # SIDE
        # ================================================

        return self.side_armor, "SIDE"
    
    # =====================================================
    # HIT
    # =====================================================

    def take_hit(
        self,
        penetration,
        projectile_angle
    ):

        armor, zone = self.get_hit_armor(
            projectile_angle
        )

        # ================================================
        # PENETRATION
        # ================================================

        if penetration >= armor:

            self.alive = False

            print(
                f"PENETRATION: {zone}"
            )

        else:

            print(
                f"BOUNCE: {zone}"
            )

        return penetration >= armor
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        if not self.alive:

            screen_x, screen_y = camera.apply(
                self.x,
                self.y
            )

            pygame.draw.circle(
                surface,
                (255, 80, 40),
                (
                    int(screen_x + TILE_SIZE // 2),
                    int(screen_y + TILE_SIZE // 2)
                ),
                8
            )

            return

        screen_x, screen_y = camera.apply(
            self.x,
            self.y
        )

        # =================================================
        # HULL SURFACE
        # =================================================

        hull_surface = pygame.Surface(
            (16, 16),
            pygame.SRCALPHA
        )

        # =================================================
        # HULL
        # =================================================

        pygame.draw.rect(
            hull_surface,
            (110, 95, 75),
            (2, 2, 12, 12)
        )

        # =================================================
        # TRACKS
        # =================================================

        pygame.draw.rect(
            hull_surface,
            (45, 45, 45),
            (0, 2, 2, 12)
        )

        pygame.draw.rect(
            hull_surface,
            (45, 45, 45),
            (14, 2, 2, 12)
        )

        # =================================================
        # REAR GRILL
        # =================================================

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (3, 5, 2, 6)
        )

        # =================================================
        # EXHAUSTS
        # =================================================

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (1, 3, 2, 2)
        )

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (1, 11, 2, 2)
        )

        # =================================================
        # ROTATION
        # =================================================

        angle_map = {

            "N": 90,
            "NE": 45,
            "E": 0,
            "SE": -45,
            "S": -90,
            "SW": -135,
            "W": 180,
            "NW": 135,
        }

        rotated_hull = pygame.transform.rotate(
            hull_surface,
            angle_map[self.visual_facing]
        )

        hull_rect = rotated_hull.get_rect(
            center=(
                screen_x + TILE_SIZE // 2,
                screen_y + TILE_SIZE // 2
            )
        )

        surface.blit(
            rotated_hull,
            hull_rect
        )

        # =================================================
        # TURRET
        # =================================================

        center_x = (
            screen_x + TILE_SIZE // 2
        )

        center_y = (
            screen_y + TILE_SIZE // 2
        )

        angle = TURRET_DIRECTIONS[
            self.turret_index
        ]

        radians = math.radians(angle)

        turret_length = 10

        end_x = (
            center_x +
            math.cos(radians) *
            turret_length
        )

        end_y = (
            center_y +
            math.sin(radians) *
            turret_length
        )

        pygame.draw.line(
            surface,
            (60, 60, 60),
            (center_x, center_y),
            (end_x, end_y),
            2
        )

        pygame.draw.circle(
            surface,
            (90, 90, 90),
            (center_x, center_y),
            3
        )