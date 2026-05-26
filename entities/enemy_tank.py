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
        
        # =================================================
        # AI
        # =================================================

        self.detection_range = 220

        self.reload_timer = 0
        self.reload_time = 1.8

    
    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        player
    ):

        if not self.alive:
            return

        if not self.can_see_player(player):
            return

        self.aim_turret_at_player(
            player
        )

        self.try_fire_at_player(
            dt,
            player
        )

        self.update_projectiles(
            dt,
            [player]
        )
    
    # =====================================================
    # DETECTION
    # =====================================================

    def can_see_player(
        self,
        player
    ):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        return distance <= self.detection_range
    
    # =====================================================
    # AIM
    # =====================================================

    def aim_turret_at_player(
        self,
        player
    ):

        dx = player.x - self.x
        dy = player.y - self.y

        angle = math.degrees(
            math.atan2(dy, dx)
        )

        if angle < 0:
            angle += 360

        closest_index = 0
        closest_diff = 999

        for i, turret_angle in enumerate(
            TURRET_DIRECTIONS
        ):

            diff = abs(
                (angle - turret_angle + 180) % 360 - 180
            )

            if diff < closest_diff:

                closest_diff = diff
                closest_index = i

        self.turret_index = closest_index
    
    # =====================================================
    # FIRE CONTROL
    # =====================================================

    def try_fire_at_player(
        self,
        dt,
        player
    ):

        self.reload_timer -= dt

        if self.reload_timer > 0:
            return

        self.reload_timer = self.reload_time

        self.fire_shell()
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        super().draw(surface, camera)

        