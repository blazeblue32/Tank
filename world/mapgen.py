import random

from core.constants import *

def grow_forest_patch(
    tiles,
    start_x,
    start_y,
    size
):

    frontier = [
        (start_x, start_y)
    ]

    visited = set()

    while frontier:

        x, y = frontier.pop(0)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (
            x < 0 or
            y < 0 or
            x >= MAP_WIDTH or
            y >= MAP_HEIGHT
        ):
            continue

        # =====================================
        # PLACE FOREST
        # =====================================

        tiles[y][x] = TERRAIN_FOREST

        # =====================================
        # PATCH GROWTH
        # =====================================

        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1)
        ]:

            nx = x + dx
            ny = y + dy

            if (nx, ny) in visited:
                continue

            # ================================
            # DISTANCE DECAY
            # ================================

            distance = (
                abs(nx - start_x) +
                abs(ny - start_y)
            )

            growth_chance = max(
                0.15,
                1.0 -
                (distance / size)
            )

            if random.random() < growth_chance:

                frontier.append(
                    (nx, ny)
                )

def generate_map():

    tiles = []

    for y in range(MAP_HEIGHT):

        row = []

        for x in range(MAP_WIDTH):

            terrain = TERRAIN_GRASS

            r = random.random()

            if r < 0.04:
                terrain = TERRAIN_MUD

            row.append(terrain)

        tiles.append(row)

    # =============================================
    # FOREST PATCHES
    # =============================================

    forest_patches = 16

    for _ in range(forest_patches):

        start_x = random.randint(
            0,
            MAP_WIDTH - 1
        )

        start_y = random.randint(
            0,
            MAP_HEIGHT - 1
        )

        size = random.randint(
            6,
            14
        )

        grow_forest_patch(
            tiles,
            start_x,
            start_y,
            size
        )

    # =====================================================
    # River
    # =====================================================

    river_tiles = []

    river_x = MAP_WIDTH // 2

    for y in range(MAP_HEIGHT):

        width = random.randint(2, 4)

        for rx in range(width):

            tx = river_x + rx

            if 0 <= tx < MAP_WIDTH:

                tiles[y][tx] = TERRAIN_WATER

                river_tiles.append((tx, y))

        river_x += random.randint(-1, 1)

        river_x = max(5, min(MAP_WIDTH - 5, river_x))

    # =====================================================
    # Main road
    # =====================================================

    road_y = MAP_HEIGHT // 2

    for x in range(MAP_WIDTH):

        if tiles[road_y][x] != TERRAIN_WATER:
            tiles[road_y][x] = TERRAIN_ROAD

    # =====================================================
    # Bridge objects
    # =====================================================

    bridges = []

    for x in range(MAP_WIDTH):

        if tiles[road_y][x] == TERRAIN_WATER:

            bridges.append({
                "x": x,
                "y": road_y,
                "destroyed": False
            })

    return tiles, bridges
    
