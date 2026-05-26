from entities.tank_base import TankBase

from systems.movement import *
from core.constants import *

import pygame

class PlayerTank(TankBase):

    def __init__(self, tilemap):

        super().__init__(tilemap)

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
        
        self.update_floating_texts(dt)

    # =====================================================
    # INPUT
    # =====================================================

    def handle_input(self):

        just_pressed = get_just_pressed_direction()

        held_direction = get_held_direction()

        # ================================================
        # CONTINUOUS FORWARD MOVEMENT
        # ================================================

        if held_direction == self.hull_direction:

            self.clear_reverse_buffer()

            self.try_begin_move(
                held_direction,
                reverse=False
            )

            return

        # ================================================
        # CONTINUOUS REVERSE MOVEMENT
        # ================================================

        if (
            held_direction ==
            opposite_direction(self.hull_direction)
            and
            just_pressed is None
            and
            not self.reverse_pending
        ):

            self.try_begin_move(
                held_direction,
                reverse=True
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

        if direction == opposite_direction(self.hull_direction):

            if (
                self.reverse_pending and
                self.reverse_pending_direction == direction
            ):

                self.clear_reverse_buffer()

                self.begin_turn(direction)

                return

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
    # TURRET
    # =====================================================

    def update_turret(self):

        keys = pygame.key.get_pressed()

        left_pressed = keys[pygame.K_LEFT]
        right_pressed = keys[pygame.K_RIGHT]

        current_index = (
            DIRECTIONS.index(
                self.turret_direction
            )
        )

        if left_pressed and not self.left_pressed_last:

            current_index -= 1
            current_index %= 8

            self.turret_direction = (
                DIRECTIONS[
                    current_index
                ]
            )

        if right_pressed and not self.right_pressed_last:

            current_index += 1
            current_index %= 8

            self.turret_direction = (
                DIRECTIONS[
                    current_index
                ]
            )

        self.left_pressed_last = left_pressed
        self.right_pressed_last = right_pressed

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