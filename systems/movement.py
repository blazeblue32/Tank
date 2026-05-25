import pygame

from core.constants import *
from world.terrain import *

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

def get_input_direction():

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        return "up"

    if keys[pygame.K_s]:
        return "down"

    if keys[pygame.K_a]:
        return "left"

    if keys[pygame.K_d]:
        return "right"

    return None