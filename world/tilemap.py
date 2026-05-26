import random

from core.constants import *
from world.mapgen import generate_map
from world.terrain import *

class TileMap:

    def __init__(self):

        self.tiles, self.bridges = generate_map()

        # =================================================
        # TERRAIN DAMAGE
        # =================================================

        self.ground_damage = {}

        # =================================================
        # VISUAL CRATERS
        # =================================================

        self.crater_marks = {}
        
        # =================================================
        # WRECKS
        # =================================================

        self.wrecks = []

    # =====================================================
    # TILE ACCESS
    # =====================================================

    def get_tile(self, x, y):

        if y < 0 or y >= len(self.tiles):
            return None

        if x < 0 or x >= len(self.tiles[0]):
            return None

        return self.tiles[y][x]

    # =====================================================
    # BRIDGES
    # =====================================================

    def has_bridge(self, x, y):

        for bridge in self.bridges:

            if bridge["destroyed"]:
                continue

            if bridge["x"] == x and bridge["y"] == y:
                return True

        return False

    # =====================================================
    # DAMAGE
    # =====================================================

    def add_ground_damage(
        self,
        x,
        y,
        amount
    ):

        key = (x, y)

        current = self.ground_damage.get(key, 0)

        current += amount

        current = min(1.0, current)

        self.ground_damage[key] = current

    # =====================================================
    # RADIAL DAMAGE
    # =====================================================

    def add_radial_ground_damage(
        self,
        center_x,
        center_y,
        radius,
        center_damage
    ):

        for y in range(
            center_y - radius,
            center_y + radius + 1
        ):

            for x in range(
                center_x - radius,
                center_x + radius + 1
            ):

                dx = x - center_x
                dy = y - center_y

                distance = (
                    dx * dx + dy * dy
                ) ** 0.5

                if distance > radius:
                    continue

                # =========================================
                # FALLOFF
                # =========================================

                falloff = 1.0 - (
                    distance / radius
                )

                damage = (
                    center_damage *
                    falloff
                )

                terrain = self.get_tile(x, y)
                
                if terrain is None:
                    continue

                if not terrain_craterable(
                    terrain
                ):
                    continue

                self.add_ground_damage(
                    x,
                    y,
                    damage
                )

    # =====================================================
    # CRATER MARKS
    # =====================================================

    def add_crater_mark(
        self,
        tile_x,
        tile_y,
        radius_min=2,
        radius_max=4
    ):

        key = (tile_x, tile_y)

        if key not in self.crater_marks:

            self.crater_marks[key] = []

        crater = {

            "x": random.randint(2, 14),

            "y": random.randint(2, 14),

            "radius": random.randint(
                radius_min,
                radius_max
            )
        }

        self.crater_marks[key].append(
            crater
        )

    def get_crater_marks(self, x, y):

        return self.crater_marks.get(
            (x, y),
            []
        )

    # =====================================================
    # ACCESS
    # =====================================================

    def get_ground_damage(self, x, y):

        return self.ground_damage.get(
            (x, y),
            0
        )
        
# =====================================================
# OBSTRUCTION TRACE
# =====================================================

    def calculate_obstruction_between(
        self,
        x1,
        y1,
        x2,
        y2
    ):

        obstruction = 0.0

        dx = x2 - x1
        dy = y2 - y1

        steps = max(
            abs(dx),
            abs(dy)
        )

        if steps == 0:
            return 0.0

        step_x = dx / steps
        step_y = dy / steps

        current_x = x1
        current_y = y1

        for _ in range(int(steps)):

            tile_x = int(current_x)
            tile_y = int(current_y)

            terrain = self.get_tile(
                tile_x,
                tile_y
            )

            if terrain is not None:

                obstruction += terrain_obstruction(
                    terrain
                )

            # =============================================
            # WRECKS
            # =============================================

            for wreck in self.wrecks:

                if (
                    wreck.tile_x == tile_x
                    and
                    wreck.tile_y == tile_y
                ):

                    obstruction += 1.0

            current_x += step_x
            current_y += step_y

        return obstruction