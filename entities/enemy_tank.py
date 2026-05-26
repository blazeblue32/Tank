import pygame
import math

from core.constants import *
from entities.tank_base import TankBase
from systems.movement import *
from world.terrain import *
from systems.visibility import *

class EnemyTank(TankBase):

    def __init__(
        self,
        tilemap,
        x,
        y
    ):

        super().__init__(tilemap)

        self.tile_x = x // TILE_SIZE
        self.tile_y = y // TILE_SIZE

        self.x = self.tile_x * TILE_SIZE
        self.y = self.tile_y * TILE_SIZE
        
        # =================================================
        # AI
        # =================================================

        self.detection_range = 220

        self.reload_timer = 0
        
        self.reload_time = 2.5
        
        self.preferred_range = 96

        self.minimum_range = 64

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        player
    ):

        self.update_particles(dt)

        self.update_projectiles(
            dt,
            [player]
        )
        
        self.update_floating_texts(dt)

        if not self.alive:
            return

        self.update_turning(dt)

        if self.moving:
            self.update_movement(dt)

        visible = can_see(
            self,
            player
        )

        if visible:

            self.update_hull_rotation(
                player
            )

            self.update_movement_ai(
                player
            )

            self.aim_turret_at_player(
                player
            )

            self.try_fire_at_player(
                dt,
                player
            )

        self.update_particles(dt)

        self.update_projectiles(
            dt,
            [player]
        )
    
    # =====================================================
    # DETECTION
    # =====================================================
        
    def distance_to_player(
        self,
        player
    ):

        dx = player.x - self.x
        dy = player.y - self.y

        return math.sqrt(
            dx * dx +
            dy * dy
        )
    
    def get_detection_range(
        self,
        player
    ):

        tile = self.tilemap.get_tile(
            player.tile_x,
            player.tile_y
        )

        detection = self.detection_range

        # ================================================
        # FOREST CONCEALMENT
        # ================================================

        concealment = terrain_concealment(
            tile
        )

        detection *= (
            1.0 - concealment
        )

        return detection
    
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

        for i, direction in enumerate(
            DIRECTIONS
        ):

            turret_angle = DIRECTION_ANGLES[
                direction
            ]

            diff = abs(
                (
                    angle -
                    turret_angle +
                    180
                ) % 360 - 180
            )

            if diff < closest_diff:

                closest_diff = diff
                closest_index = i

        self.turret_direction = (
            DIRECTIONS[
                closest_index
            ]
        )
    
    # =====================================================
    # HULL AIM
    # =====================================================

    def get_direction_to_player(
        self,
        player
    ):

        dx = player.x - self.x
        dy = player.y - self.y

        # ================================================
        # CARDINAL PRIORITY
        # ================================================

        if abs(dx) > abs(dy):

            if dx > 0:
                return "E"
            else:
                return "W"

        else:

            if dy > 0:
                return "S"
            else:
                return "N"
    
    # =====================================================
    # HULL CONTROL
    # =====================================================

    def update_hull_rotation(
        self,
        player
    ):

        if self.turning:
            return

        desired = self.get_direction_to_player(
            player
        )

        if desired == self.hull_direction:
            return

        self.begin_turn(desired)
    
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
    # MOVEMENT AI
    # =====================================================

    def update_movement_ai(
        self,
        player
    ):

        if self.turning:
            return

        if self.moving:
            return

        desired = self.get_direction_to_player(
            player
        )

        distance = self.distance_to_player(
            player
        )

        # ================================================
        # TOO FAR
        # ================================================

        if distance > self.preferred_range:

            if desired != self.hull_direction:

                self.begin_turn(desired)
                return

            self.try_begin_move(
                self.hull_direction,
                reverse=False
            )

            return

        # ================================================
        # TOO CLOSE
        # ================================================

        if distance < self.minimum_range:

            if desired != self.hull_direction:

                self.begin_turn(desired)
                return

            reverse_direction = opposite_direction(
                self.hull_direction
            )

            self.try_begin_move(
                reverse_direction,
                reverse=True
            )
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        super().draw(surface, camera)

        