import pygame
import math

from core.constants import *
from systems.movement import *
from world.terrain import *

class Tank:

    def __init__(self, tilemap):

        self.tilemap = tilemap

        # ==========================================
        # Tile position
        # ==========================================

        self.tile_x = 10
        self.tile_y = 10

        # ==========================================
        # World position
        # ==========================================

        self.x = self.tile_x * TILE_SIZE
        self.y = self.tile_y * TILE_SIZE

        # ==========================================
        # Movement
        # ==========================================

        self.target_tile_x = self.tile_x
        self.target_tile_y = self.tile_y

        self.moving = False

        self.direction = "down"
        self.queued_direction = None

        self.base_speed = 90

        # ==========================================
        # Turret
        # ==========================================

        self.turret_angle = 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        self.update_turret(dt)

        input_direction = get_input_direction()

        if input_direction:
            self.queued_direction = input_direction

        if not self.moving and self.queued_direction:
            self.try_begin_move(self.queued_direction)

        if self.moving:
            self.update_movement(dt)

    # =====================================================
    # TURRET
    # =====================================================

    def update_turret(self, dt):

        keys = pygame.key.get_pressed()

        rotation_speed = 180

        if keys[pygame.K_LEFT]:
            self.turret_angle -= rotation_speed * dt

        if keys[pygame.K_RIGHT]:
            self.turret_angle += rotation_speed * dt

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

        if not terrain_passable(terrain):
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

        if distance < 1:

            self.x = target_x
            self.y = target_y

            self.tile_x = self.target_tile_x
            self.tile_y = self.target_tile_y

            self.moving = False

            if self.queued_direction:
                self.try_begin_move(self.queued_direction)

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

        # ==========================================
        # Hull
        # ==========================================

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

        # ==========================================
        # Turret
        # ==========================================

        center_x = screen_x + TILE_SIZE // 2
        center_y = screen_y + TILE_SIZE // 2

        pygame.draw.circle(
            surface,
            TANK_TURRET,
            (int(center_x), int(center_y)),
            4
        )

        # ==========================================
        # Barrel
        # ==========================================

        radians = math.radians(self.turret_angle)

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