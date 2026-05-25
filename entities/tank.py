import pygame
import math

from core.constants import *
from systems.movement import *
from world.terrain import *

class Tank:

    def __init__(self, tilemap):

        self.tilemap = tilemap

        # =================================================
        # TILE POSITION
        # =================================================

        self.tile_x = 10
        self.tile_y = 10

        # =================================================
        # WORLD POSITION
        # =================================================

        self.x = self.tile_x * TILE_SIZE
        self.y = self.tile_y * TILE_SIZE

        # =================================================
        # MOVEMENT
        # =================================================

        self.target_tile_x = self.tile_x
        self.target_tile_y = self.tile_y

        self.moving = False

        self.direction = "down"

        self.base_speed = 22

        # =================================================
        # TURRET
        # =================================================

        self.turret_index = 0

        self.left_pressed_last = False
        self.right_pressed_last = False

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        self.update_turret()

        if not self.moving:

            direction = get_input_direction()

            if direction:
                self.try_begin_move(direction)

        if self.moving:
            self.update_movement(dt)

    # =====================================================
    # TURRET
    # =====================================================

    def update_turret(self):

        keys = pygame.key.get_pressed()

        left_pressed = keys[pygame.K_LEFT]
        right_pressed = keys[pygame.K_RIGHT]

        if left_pressed and not self.left_pressed_last:

            self.turret_index -= 1
            self.turret_index %= 8

        if right_pressed and not self.right_pressed_last:

            self.turret_index += 1
            self.turret_index %= 8

        self.left_pressed_last = left_pressed
        self.right_pressed_last = right_pressed

    # =====================================================
    # MOVEMENT
    # =====================================================

    def try_begin_move(self, direction):

        dx, dy = DIRECTION_VECTORS[direction]

        new_x = self.tile_x + dx
        new_y = self.tile_y + dy

        terrain = self.tilemap.get_tile(new_x, new_y)

        if terrain is None:
            return

        # =================================================
        # WATER CHECK
        # =================================================

        if terrain == TERRAIN_WATER:

            if not self.tilemap.has_bridge(new_x, new_y):
                return

        elif not terrain_passable(terrain):
            return

        self.target_tile_x = new_x
        self.target_tile_y = new_y

        self.direction = direction
        self.moving = True

    def update_movement(self, dt):

        target_x = self.target_tile_x * TILE_SIZE
        target_y = self.target_tile_y * TILE_SIZE

        terrain = self.tilemap.get_tile(
            self.target_tile_x,
            self.target_tile_y
        )

        speed_mod = terrain_speed_modifier(terrain)

        move_speed = self.base_speed * speed_mod

        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.5:

            self.x = target_x
            self.y = target_y

            self.tile_x = self.target_tile_x
            self.tile_y = self.target_tile_y

            self.moving = False

            return

        move_x = (dx / distance) * move_speed * dt
        move_y = (dy / distance) * move_speed * dt

        self.x += move_x
        self.y += move_y

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        screen_x, screen_y = camera.apply(self.x, self.y)

        # =================================================
        # HULL
        # =================================================

        body_rect = pygame.Rect(
            screen_x + 2,
            screen_y + 2,
            TILE_SIZE - 4,
            TILE_SIZE - 4
        )

        pygame.draw.rect(
            surface,
            TANK_BODY,
            body_rect
        )

        # =================================================
        # TURRET
        # =================================================

        center_x = screen_x + TILE_SIZE // 2
        center_y = screen_y + TILE_SIZE // 2

        pygame.draw.circle(
            surface,
            TANK_TURRET,
            (int(center_x), int(center_y)),
            4
        )

        angle = TURRET_DIRECTIONS[self.turret_index]

        radians = math.radians(angle)

        barrel_length = 10

        end_x = center_x + math.cos(radians) * barrel_length
        end_y = center_y + math.sin(radians) * barrel_length

        pygame.draw.line(
            surface,
            TANK_TURRET,
            (center_x, center_y),
            (end_x, end_y),
            2
        )