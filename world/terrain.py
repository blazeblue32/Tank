from core.constants import *

def terrain_speed_modifier(terrain_type):

    return TERRAIN_DATA[terrain_type]["speed"]

def terrain_passable(terrain_type):

    return TERRAIN_DATA[terrain_type]["passable"]