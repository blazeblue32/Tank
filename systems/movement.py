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

def get_pressed_direction():

    keys = pygame.key.get_pressed()

    for key, direction in DIRECTION_KEYS.items():

        if keys[key]:
            return direction

    return None

def opposite_direction(direction):

    return (direction + 2) % 4