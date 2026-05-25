import pygame
import math

from core.constants import *

class EnemyTank:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        # =================================================
        # FACING
        # =================================================

        self.hull_facing = EAST

        self.visual_facing = "E"

        self.turret_index = 0

        # =================================================
        # STATE
        # =================================================

        self.alive = True

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        pass

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        if not self.alive:
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