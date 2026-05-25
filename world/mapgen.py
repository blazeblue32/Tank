import random

from core.constants import *

def generate_map():

    tiles = []

    for y in range(MAP_HEIGHT):

        row = []

        for x in range(MAP_WIDTH):

            terrain = TERRAIN_GRASS

            r = random.random()

            if r < 0.08:
                terrain = TERRAIN_FOREST

            elif r < 0.12:
                terrain = TERRAIN_MUD

            row.append(terrain)

        tiles.append(row)

    # =====================================================
    # Create river
    # =====================================================

    river_x = MAP_WIDTH // 2

    for y in range(MAP_HEIGHT):

        width = random.randint(2, 4)

        for rx in range(width):

            if 0 <= river_x + rx < MAP_WIDTH:
                tiles[y][river_x + rx] = TERRAIN_WATER

        river_x += random.randint(-1, 1)

        river_x = max(5, min(MAP_WIDTH - 5, river_x))

    # =====================================================
    # Create horizontal road
    # =====================================================

    road_y = MAP_HEIGHT // 2

    for x in range(MAP_WIDTH):

        tiles[road_y][x] = TERRAIN_ROAD

    # =====================================================
    # Create bridge
    # =====================================================

    for bx in range(MAP_WIDTH):

        if tiles[road_y][bx] == TERRAIN_WATER:
            tiles[road_y][bx] = TERRAIN_ROAD

    return tiles