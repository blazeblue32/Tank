import pygame

from core.constants import *

DIRECTION_KEYS = {
    pygame.K_w: NORTH,
    pygame.K_d: EAST,
    pygame.K_s: SOUTH,
    pygame.K_a: WEST,
}

CARDINAL_VECTORS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}

previous_keys = None

# =========================================================
# INPUT UPDATE
# =========================================================

def update_input_state():

    global previous_keys

    if previous_keys is None:
        previous_keys = pygame.key.get_pressed()

# =========================================================
# JUST PRESSED
# =========================================================

def get_just_pressed_direction():

    global previous_keys

    keys = pygame.key.get_pressed()

    for key, direction in DIRECTION_KEYS.items():

        if keys[key] and not previous_keys[key]:

            previous_keys = keys

            return direction

    previous_keys = keys

    return None

# =========================================================
# HELD DIRECTION
# =========================================================

def get_held_direction():

    keys = pygame.key.get_pressed()

    for key, direction in DIRECTION_KEYS.items():

        if keys[key]:
            return direction

    return None

# =========================================================
# OPPOSITE
# =========================================================

def opposite_direction(direction):

    return (direction + 2) % 4