import pygame
import math
import random

from core.constants import *
from systems.movement import *
from world.terrain import *
from entities.particle import SmokeParticle
from entities.projectile import Projectile

class TankBase:

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

        self.hull_facing = EAST

        self.visual_facing = "E"

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

        self.fire_cooldown = 2.5

        self.fire_timer = 0
        
        # =================================================
        # STATE
        # =================================================

        self.alive = True

        self.destroyed = False
        
        # =================================================
        # ARMOR
        # =================================================

        self.front_armor = 3
        
        self.side_armor = 2
        
        self.rear_armor = 1

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dt,
        enemy_tanks
    ):

        self.update_turret()

        self.update_turning(dt)
        
        self.update_reverse_buffer(dt)

        if not self.turning and not self.moving:
            self.handle_input()

        if self.moving:
            self.update_movement(dt)

        self.update_particles(dt)
        
        self.update_projectiles(
            dt,
            enemy_tanks
        )

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

        # ================================================
        # WRECK BLOCKING
        # ================================================

        for wreck in getattr(
            self.tilemap,
            "wrecks",
            []
        ):

            if (
                wreck.tile_x == new_x
                and
                wreck.tile_y == new_y
            ):

                return

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
            self.tilemap,
            self
        )

        self.projectiles.append(projectile)

    # =====================================================
    # PROJECTILES
    # =====================================================

    def update_projectiles(
        self,
        dt,
        enemy_tanks
    ):

        for projectile in self.projectiles:

            projectile.update(dt)

            projectile.check_tank_collision(
                enemy_tanks
            )

        self.projectiles = [

            p for p in self.projectiles

            if (
                not p.dead or
                len(p.impact_particles) > 0 or
                len(p.impact_flashes) > 0
            )
        ]
    
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
            
            self.destroyed = True
            
            if self not in self.tilemap.wrecks:

                self.tilemap.wrecks.append(
                    self
                )

        return penetration >= armor
    
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
        # DESTROYED / WRECK
        # =================================================

        if self.destroyed:

            screen_x, screen_y = camera.apply(
                self.x,
                self.y
            )

            wreck_surface = pygame.Surface(
                (16, 16),
                pygame.SRCALPHA
            )

            # =============================================
            # BURNT HULL
            # =============================================

            pygame.draw.rect(
                wreck_surface,
                (45, 45, 45),
                (1, 3, 14, 10)
            )

            # =============================================
            # INNER DAMAGE
            # =============================================

            pygame.draw.rect(
                wreck_surface,
                (25, 25, 25),
                (4, 4, 8, 8)
            )

            # =============================================
            # TRACKS
            # =============================================

            pygame.draw.rect(
                wreck_surface,
                (20, 20, 20),
                (1, 1, 14, 2)
            )

            pygame.draw.rect(
                wreck_surface,
                (20, 20, 20),
                (1, 13, 14, 2)
            )

            # =============================================
            # DAMAGED TURRET
            # =============================================

            pygame.draw.circle(
                wreck_surface,
                (35, 35, 35),
                (8, 8),
                3
            )

            pygame.draw.line(
                wreck_surface,
                (15, 15, 15),
                (8, 8),
                (13, 5),
                2
            )

            angle = VISUAL_ANGLES[
                self.visual_facing
            ]

            rotated = pygame.transform.rotate(
                wreck_surface,
                -angle
            )

            rect = rotated.get_rect(
                center=(
                    screen_x + TILE_SIZE // 2,
                    screen_y + TILE_SIZE // 2
                )
            )

            surface.blit(
                rotated,
                rect
            )

            return

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
            (110, 95, 75),
            (1, 3, 14, 10)
        )
        
        # =================================================
        # TRACKS
        # =================================================

        pygame.draw.rect(
            hull_surface,
            (45, 45, 45),
            (1, 1, 14, 2)
        )

        pygame.draw.rect(
            hull_surface,
            (45, 45, 45),
            (1, 13, 14, 2)
        )

        # ================================================
        # ENGINE GRILL
        # ================================================

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (2, 5, 2, 6)
        )

        # ================================================
        # EXHAUSTS
        # ================================================

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (0, 4, 2, 2)
        )

        pygame.draw.rect(
            hull_surface,
            BLACK,
            (0, 10, 2, 2)
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