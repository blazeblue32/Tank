from core.constants import *
from world.terrain_data import TERRAIN_TYPES


# =====================================================
# ACCESS
# =====================================================


def get_terrain_data(terrain):

    return TERRAIN_TYPES[terrain]


# =====================================================
# HELPERS
# =====================================================


def terrain_color(terrain):

    return get_terrain_data(terrain)["color"]



def terrain_speed_modifier(terrain):

    return get_terrain_data(terrain)["speed"]



def terrain_passable(terrain):

    return get_terrain_data(terrain)["passable"]



def terrain_concealment(terrain):

    return get_terrain_data(terrain)["concealment"]



def terrain_obstruction(terrain):

    return get_terrain_data(terrain)["obstruction"]



def terrain_vision_block(terrain):

    return get_terrain_data(terrain)["vision_block"]



def terrain_craterable(terrain):

    return get_terrain_data(terrain)["craterable"]



def terrain_type(terrain):

    return get_terrain_data(terrain)["type"]
    
# =====================================================
# OBSTRUCTION
# =====================================================

def terrain_obstruction(terrain):

    return get_terrain_data(
        terrain
    )["obstruction"]