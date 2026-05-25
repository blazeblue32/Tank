import pygame

# =========================================================
# DISPLAY
# =========================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TILE_SIZE = 16

MAP_WIDTH = 100
MAP_HEIGHT = 100

# =========================================================
# COLORS
# =========================================================

BLACK = (0, 0, 0)

GRASS = (74, 124, 89)
FOREST = (38, 79, 52)
ROAD = (120, 104, 84)
MUD = (92, 74, 58)
WATER = (48, 80, 120)

BRIDGE = (160, 140, 90)

TANK_BODY = (210, 210, 180)
TANK_TURRET = (240, 240, 220)

GRID = (0, 0, 0)

# =========================================================
# TERRAIN TYPES
# =========================================================

TERRAIN_GRASS = 0
TERRAIN_FOREST = 1
TERRAIN_ROAD = 2
TERRAIN_MUD = 3
TERRAIN_WATER = 4

# =========================================================
# TERRAIN DATA
# =========================================================

TERRAIN_DATA = {

    TERRAIN_GRASS: {
        "color": GRASS,
        "speed": 1.0,
        "passable": True,
    },

    TERRAIN_FOREST: {
        "color": FOREST,
        "speed": 0.7,
        "passable": True,
    },

    TERRAIN_ROAD: {
        "color": ROAD,
        "speed": 1.35,
        "passable": True,
    },

    TERRAIN_MUD: {
        "color": MUD,
        "speed": 0.45,
        "passable": True,
    },

    TERRAIN_WATER: {
        "color": WATER,
        "speed": 0.0,
        "passable": False,
    },
}

# =========================================================
# TURRET DIRECTIONS
# 8-direction snapped aiming
# =========================================================

TURRET_DIRECTIONS = [
    0,
    45,
    90,
    135,
    180,
    225,
    270,
    315,
]