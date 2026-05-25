from world.mapgen import generate_map

class TileMap:

    def __init__(self):

        self.tiles, self.bridges = generate_map()

        # =================================================
        # TERRAIN DAMAGE
        # =================================================

        self.ground_damage = {}

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
    # GROUND DAMAGE
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

    def get_ground_damage(self, x, y):

        return self.ground_damage.get((x, y), 0)