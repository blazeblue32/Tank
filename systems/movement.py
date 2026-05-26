import pygame

from core.constants import *

DIRECTION_KEYS = {
    pygame.K_w: "N",
    pygame.K_d: "E",
    pygame.K_s: "S",
    pygame.K_a: "W",
}

CARDINAL_VECTORS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
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

    opposites = {

        "N": "S",
        "E": "W",
        "S": "N",
        "W": "E",
    }

    return opposites[
        direction
    ]