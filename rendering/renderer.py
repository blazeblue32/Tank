import pygame

from core.constants import *

class Renderer:

    def draw_map(self, surface, tilemap, camera):

        visible_tiles_x = SCREEN_WIDTH // TILE_SIZE + 2
        visible_tiles_y = SCREEN_HEIGHT // TILE_SIZE + 2

        start_x = int(camera.x // TILE_SIZE)
        start_y = int(camera.y // TILE_SIZE)

        for y in range(start_y, start_y + visible_tiles_y):

            for x in range(start_x, start_x + visible_tiles_x):

                tile = tilemap.get_tile(x, y)

                if tile is None:
                    continue

                color = TERRAIN_DATA[tile]["color"]

                damage = tilemap.get_ground_damage(x, y)

                # =========================================
                # DARKEN DAMAGED GROUND
                # =========================================

                if damage > 0:

                    darkness = int(damage * 40)

                    color = (
                        max(0, color[0] - darkness),
                        max(0, color[1] - darkness),
                        max(0, color[2] - darkness),
                    )

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

                # =========================================
                # DAMAGE MARK
                # =========================================

                if damage > 0.2:

                    pygame.draw.circle(
                        surface,
                        (40, 30, 30),
                        (
                            screen_x + TILE_SIZE // 2,
                            screen_y + TILE_SIZE // 2
                        ),
                        int(2 + damage * 4)
                    )

                pygame.draw.rect(
                    surface,
                    GRID,
                    rect,
                    1
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