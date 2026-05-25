from world.mapgen import generate_map

class TileMap:

    def __init__(self):

        self.tiles, self.bridges = generate_map()

    def get_tile(self, x, y):

        if y < 0 or y >= len(self.tiles):
            return None

        if x < 0 or x >= len(self.tiles[0]):
            return None

        return self.tiles[y][x]

    # =====================================================
    # BRIDGE CHECK
    # =====================================================

    def has_bridge(self, x, y):

        for bridge in self.bridges:

            if bridge["destroyed"]:
                continue

            if bridge["x"] == x and bridge["y"] == y:
                return True

        return False