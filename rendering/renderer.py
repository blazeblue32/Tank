import pygame

from core.constants import *

class Renderer:

    def draw_map(self, surface, tilemap, camera):

        visible_tiles_x = SCREEN_WIDTH // TILE_SIZE + 2
        visible_tiles_y = SCREEN_HEIGHT // TILE_SIZE + 2

        start_x = int(camera.x // TILE_SIZE)
        start_y = int(camera.y // TILE_SIZE)

        # =================================================
        # BASE TERRAIN
        # =================================================

        for y in range(start_y, start_y + visible_tiles_y):

            for x in range(start_x, start_x + visible_tiles_x):

                tile = tilemap.get_tile(x, y)

                if tile is None:
                    continue

                color = TERRAIN_DATA[tile]["color"]

                screen_x, screen_y = camera.apply(
                    x * TILE_SIZE,
                    y * TILE_SIZE
                )

                rect = pygame.Rect(
                    screen_x,
                    screen_y,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pygame.draw.rect(
                    surface,
                    color,
                    rect
                )

        # =================================================
        # CRATER MARKS
        # =================================================

        for y in range(start_y, start_y + visible_tiles_y):

            for x in range(start_x, start_x + visible_tiles_x):

                crater_marks = (
                    tilemap.get_crater_marks(x, y)
                )

                if not crater_marks:
                    continue

                screen_x, screen_y = camera.apply(
                    x * TILE_SIZE,
                    y * TILE_SIZE
                )

                # =========================================
                # INDIVIDUAL CRATERS
                # =========================================

                for crater in crater_marks:

                    crater_x = (
                        screen_x + crater["x"]
                    )

                    crater_y = (
                        screen_y + crater["y"]
                    )

                    crater_radius = (
                        crater["radius"]
                    )

                    # =====================================
                    # MAIN CRATER
                    # =====================================

                    pygame.draw.circle(
                        surface,
                        CRATER,
                        (
                            crater_x,
                            crater_y
                        ),
                        crater_radius
                    )

                    # =====================================
                    # INNER CORE
                    # =====================================

                    if crater_radius >= 3:

                        pygame.draw.circle(
                            surface,
                            (55, 40, 30),
                            (
                                crater_x,
                                crater_y
                            ),
                            max(
                                1,
                                crater_radius // 2
                            )
                        )

                # =========================================
                # CONNECTED LARGE CRATERS
                # =========================================

                damage = tilemap.get_ground_damage(
                    x,
                    y
                )

                if damage < 0.8:
                    continue

                neighbors = [

                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]

                for nx, ny in neighbors:

                    neighbor_damage = (
                        tilemap.get_ground_damage(
                            nx,
                            ny
                        )
                    )

                    if neighbor_damage < 0.8:
                        continue

                    neighbor_screen_x = (
                        screen_x +
                        ((nx - x) * TILE_SIZE)
                    )

                    neighbor_screen_y = (
                        screen_y +
                        ((ny - y) * TILE_SIZE)
                    )

                    midpoint_x = (
                        screen_x +
                        neighbor_screen_x +
                        TILE_SIZE
                    ) // 2

                    midpoint_y = (
                        screen_y +
                        neighbor_screen_y +
                        TILE_SIZE
                    ) // 2

                    pygame.draw.circle(
                        surface,
                        CRATER,
                        (
                            int(midpoint_x),
                            int(midpoint_y)
                        ),
                        5
                    )

        # =================================================
        # BRIDGES
        # =================================================

        for bridge in tilemap.bridges:

            if bridge["destroyed"]:
                continue

            screen_x, screen_y = camera.apply(
                bridge["x"] * TILE_SIZE,
                bridge["y"] * TILE_SIZE
            )

            rect = pygame.Rect(
                screen_x,
                screen_y + 3,
                TILE_SIZE,
                TILE_SIZE - 6
            )

            pygame.draw.rect(
                surface,
                BRIDGE,
                rect
            )

            pygame.draw.line(
                surface,
                BLACK,
                (screen_x, screen_y + 3),
                (screen_x + TILE_SIZE, screen_y + 3),
                1
            )

            pygame.draw.line(
                surface,
                BLACK,
                (screen_x, screen_y + TILE_SIZE - 3),
                (screen_x + TILE_SIZE, screen_y + TILE_SIZE - 3),
                1
            )