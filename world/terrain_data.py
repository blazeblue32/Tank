from core.constants import *

TERRAIN_TYPES = {

    TERRAIN_GRASS: {

        "name": "Grass",

        "color": (70, 145, 60),

        "type": TERRAIN_TYPE_LAND,

        "speed": 1.0,

        "passable": True,

        "concealment": 0.0,

        "obstruction": 0.0,

        "vision_block": 0.0,

        "craterable": True,
    },

    TERRAIN_MUD: {

        "name": "Mud",

        "color": (105, 78, 52),

        "type": TERRAIN_TYPE_LAND,

        "speed": 0.7,

        "passable": True,

        "concealment": 0.0,

        "obstruction": 0.0,

        "vision_block": 0.0,

        "craterable": True,
    },

    TERRAIN_FOREST: {

        "name": "Forest",

        "color": (25, 90, 30),

        "type": TERRAIN_TYPE_LAND,

        "speed": 0.65,

        "passable": True,

        "concealment": 0.5,

        "obstruction": 1.0,

        "vision_block": 0.35,

        "craterable": True,
    },

    TERRAIN_WATER: {

        "name": "Water",

        "color": (40, 90, 200),

        "type": TERRAIN_TYPE_WATER,

        "speed": 0.0,

        "passable": False,

        "concealment": 0.0,

        "obstruction": 0.0,

        "vision_block": 0.0,

        "craterable": False,
    },
}