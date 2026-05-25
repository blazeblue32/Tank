import pygame
import math
import random

from core.constants import *
from systems.movement import *
from world.terrain import *
from entities.projectile import Projectile

from entities.particle import SmokeParticle

class Tank:

    def __init__(self, tilemap):

        self.tilemap = tilemap

        # =================================================
        # POSITION
        # =================================================

        self.tile_x = 10
        self.tile_y = 10

        self.x = self.tile_x * TILE_SIZE
        self.y = self.tile_y * TILE_SIZE

        # =================================================
        # MOVEMENT
        # =================================================

        self.target_tile_x = self.tile_x
        self.target_tile_y = self.tile_y

        self.moving = False
        self.reversing = False

        self.base_speed = 22
        self.reverse_speed = 11

        # =================================================
        # HULL FACINGS
        # =================================================

        self.hull_facing = NORTH

        self.visual_facing = "N"

        # =================================================
        # TURNING
        # =================================================

        self.turning = False

        self.turn_target = NORTH

        self.turn_timer = 0

        self.turn_duration = 1.5

        self.turn_hold_direction = None
        
        self.reverse_pending = False

        self.reverse_pending_timer = 0

        self.reverse_pending_direction = None

        self.double_tap_window = 0.25

        # =================================================
        # TURRET
        # =================================================

        self.turret_index = 0

        self.left_pressed_last = False
        self.right_pressed_last = False

        # =================================================
        # PARTICLES
        # =================================================

        self.particles = []

        self.exhaust_timer = 0

        # =================================================
        # PROJECTILES
        # =================================================

        self.projectiles = []

        self.fire_cooldown = 0.6

        self.fire_timer = 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        self.update_turret()

        self.update_turning(dt)
        
        self.update_reverse_buffer(dt)

        if not self.turning and not self.moving:
            self.handle_input()

        if self.moving:
            self.update_movement(dt)

        self.update_particles(dt)
        
        self.update_projectiles(dt)

        self.update_firing(dt)
        
    def update_reverse_buffer(self, dt):

        if not self.reverse_pending:
            return

        self.reverse_pending_timer += dt

        if self.reverse_pending_timer >= self.double_tap_window:

            self.reverse_pending = False

            self.try_begin_move(
                self.reverse_pending_direction,
                reverse=True
            )

    # =====================================================
    # INPUT
    # =====================================================

    def handle_input(self):

        just_pressed = get_just_pressed_direction()

        held_direction = get_held_direction()

        # ================================================
        # CONTINUOUS FORWARD MOVEMENT
        # ================================================

        if held_direction == self.hull_facing:

            self.clear_reverse_buffer()

            self.try_begin_move(
                held_direction,
                reverse=False
            )

            return

        # ================================================
        # NO NEW INPUT
        # ================================================

        if just_pressed is None:
            return

        direction = just_pressed

        # ================================================
        # REVERSE / 180 TURN
        # ================================================

        if direction == opposite_direction(self.hull_facing):

            # ============================================
            # SECOND TAP
            # ============================================

            if (
                self.reverse_pending and
                self.reverse_pending_direction == direction
            ):

                self.clear_reverse_buffer()

                self.begin_turn(direction)

                return

            # ============================================
            # FIRST TAP
            # ============================================

            self.reverse_pending = True

            self.reverse_pending_timer = 0

            self.reverse_pending_direction = direction

            return

        # ================================================
        # NORMAL TURN
        # ================================================

        self.clear_reverse_buffer()

        self.begin_turn(direction)

    # =====================================================
    # TURNING
    # =====================================================

    def clear_reverse_buffer(self):

        self.reverse_pending = False

        self.reverse_pending_timer = 0

        self.reverse_pending_direction = None
    
    def begin_turn(self, direction):

        self.turning = True

        self.turn_target = direction

        self.turn_timer = 0

        self.turn_hold_direction = direction

    def update_turning(self, dt):

        if not self.turning:
            return

        keys = pygame.key.get_pressed()

        held = False

        if self.turn_hold_direction == NORTH:
            held = keys[pygame.K_w]

        elif self.turn_hold_direction == EAST:
            held = keys[pygame.K_d]

        elif self.turn_hold_direction == SOUTH:
            held = keys[pygame.K_s]

        elif self.turn_hold_direction == WEST:
            held = keys[pygame.K_a]

        self.turn_timer += dt

        # ================================================
        # 180 TURN CHECK
        # ================================================

        is_180 = (
            self.turn_target ==
            opposite_direction(self.hull_facing)
        )

        if is_180:

            total_duration = self.turn_duration * 2

        else:

            total_duration = self.turn_duration

        progress = self.turn_timer / total_duration

        # ================================================
        # 90 DEGREE TURN
        # ================================================

        if not is_180:

            if progress < 0.5:

                self.visual_facing = self.get_diagonal_visual()

            else:

                self.visual_facing = self.get_cardinal_visual(
                    self.turn_target
                )

        # ================================================
        # 180 DEGREE TURN
        # ================================================

        else:

            sequence_map = {

                (NORTH, SOUTH): ["NW", "W", "SW"],
                (SOUTH, NORTH): ["SE", "E", "NE"],

                (EAST, WEST): ["NE", "N", "NW"],
                (WEST, EAST): ["SW", "S", "SE"],
            }

            sequence = sequence_map.get(
                (self.hull_facing, self.turn_target),
                ["NW", "W", "SW"]
            )

            if progress < 0.33:

                self.visual_facing = sequence[0]

            elif progress < 0.66:

                self.visual_facing = sequence[1]

            else:

                self.visual_facing = sequence[2]

        # ================================================
        # COMPLETE
        # ================================================

        if self.turn_timer >= total_duration:

            self.turning = False

            self.hull_facing = self.turn_target

            self.visual_facing = self.get_cardinal_visual(
                self.hull_facing
            )

            if held:

                self.try_begin_move(
                    self.hull_facing,
                    reverse=False
                )

    def get_diagonal_visual(self):

        pair = (self.hull_facing, self.turn_target)

        mapping = {

            (NORTH, EAST): "NE",
            (EAST, SOUTH): "SE",
            (SOUTH, WEST): "SW",
            (WEST, NORTH): "NW",

            (NORTH, WEST): "NW",
            (WEST, SOUTH): "SW",
            (SOUTH, EAST): "SE",
            (EAST, NORTH): "NE",

            # ============================================
            # 180 TURNS
            # ============================================

            (NORTH, SOUTH): "NE",
            (SOUTH, NORTH): "SW",

            (EAST, WEST): "SE",
            (WEST, EAST): "NW",
        }

        return mapping.get(pair, "N")

    def get_cardinal_visual(self, facing):

        mapping = {
            NORTH: "N",
            EAST: "E",
            SOUTH: "S",
            WEST: "W",
        }

        return mapping[facing]

    # =====================================================
    # MOVEMENT
    # =====================================================

    def try_begin_move(self, direction, reverse=False):

        dx, dy = CARDINAL_VECTORS[direction]

        new_x = self.tile_x + dx
        new_y = self.tile_y + dy

        terrain = self.tilemap.get_tile(new_x, new_y)

        if terrain is None:
            return

        # ================================================
        # BRIDGE OVERRIDE
        # ================================================

        if terrain == TERRAIN_WATER:

            if not self.tilemap.has_bridge(new_x, new_y):
                return

            speed_mod = TERRAIN_DATA[TERRAIN_ROAD]["speed"]

        else:

            if not terrain_passable(terrain):
                return

            speed_mod = terrain_speed_modifier(terrain)

        self.current_speed = self.base_speed * speed_mod

        if reverse:
            self.current_speed = self.reverse_speed * speed_mod

        self.reversing = reverse

        self.target_tile_x = new_x
        self.target_tile_y = new_y

        self.moving = True

    def update_movement(self, dt):

        target_x = self.target_tile_x * TILE_SIZE
        target_y = self.target_tile_y * TILE_SIZE

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

        move_x = (dx / distance) * self.current_speed * dt
        move_y = (dy / distance) * self.current_speed * dt

        self.x += move_x
        self.y += move_y

        self.spawn_exhaust(dt)

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
    # PARTICLES
    # =====================================================

    def spawn_exhaust(self, dt):

        self.exhaust_timer += dt

        if self.exhaust_timer < 0.05:
            return

        self.exhaust_timer = 0

        center_x = self.x + TILE_SIZE // 2
        center_y = self.y + TILE_SIZE // 2

        rear_offsets = {

            "N": [(3, 14), (11, 14)],
            "S": [(3, 2), (11, 2)],
            "E": [(2, 3), (2, 11)],
            "W": [(14, 3), (14, 11)],

            "NE": [(2, 12), (6, 14)],
            "SE": [(2, 2), (6, 0)],
            "SW": [(14, 0), (10, 2)],
            "NW": [(14, 14), (10, 12)],
        }

        offsets = rear_offsets[self.visual_facing]

        for ox, oy in offsets:

            px = self.x + ox + random.uniform(-1, 1)
            py = self.y + oy + random.uniform(-1, 1)

            self.particles.append(
                SmokeParticle(px, py)
            )

    def update_particles(self, dt):

        for particle in self.particles:
            particle.update(dt)

        self.particles = [
            p for p in self.particles
            if not p.dead
        ]

    # =====================================================
    # FIRING
    # =====================================================

    def update_firing(self, dt):

        self.fire_timer -= dt

        keys = pygame.key.get_pressed()

        if not keys[pygame.K_SPACE]:
            return

        if self.fire_timer > 0:
            return

        self.fire_timer = self.fire_cooldown

        self.fire_shell()

    def fire_shell(self):

        angle = TURRET_DIRECTIONS[
            self.turret_index
        ]

        radians = math.radians(angle)

        spawn_distance = 10

        center_x = self.x + TILE_SIZE // 2
        center_y = self.y + TILE_SIZE // 2

        spawn_x = (
            center_x +
            math.cos(radians) * spawn_distance
        )

        spawn_y = (
            center_y +
            math.sin(radians) * spawn_distance
        )

        projectile = Projectile(
            spawn_x,
            spawn_y,
            angle,
            self.tilemap
        )

        self.projectiles.append(projectile)

    # =====================================================
    # PROJECTILES
    # =====================================================

    def update_projectiles(self, dt):

        for projectile in self.projectiles:
            projectile.update(dt)

        self.projectiles = [
            p for p in self.projectiles
            if not p.dead
        ]    
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        for projectile in self.projectiles:
            projectile.draw(surface, camera)
        
        for particle in self.particles:
            particle.draw(surface, camera)

        screen_x, screen_y = camera.apply(self.x, self.y)

        # =================================================
        # HULL
        # =================================================

        angle = VISUAL_ANGLES[self.visual_facing]

        hull_surface = pygame.Surface(
            (TILE_SIZE, TILE_SIZE),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            hull_surface,
            TANK_BODY,
            (2, 2, TILE_SIZE - 4, TILE_SIZE - 4)
        )

        # ================================================
        # ENGINE GRILL
        # ================================================

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (3, 5, 2, 6)
        )

        # ================================================
        # EXHAUSTS
        # ================================================

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

        rotated = pygame.transform.rotate(
            hull_surface,
            -angle
        )

        rect = rotated.get_rect(
            center=(
                screen_x + TILE_SIZE // 2,
                screen_y + TILE_SIZE // 2
            )
        )

        surface.blit(rotated, rect)

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

        turret_angle = TURRET_DIRECTIONS[
            self.turret_index
        ]

        radians = math.radians(turret_angle)

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