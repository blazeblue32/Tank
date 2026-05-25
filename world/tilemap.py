from world.mapgen import generate_map

class TileMap:

    def __init__(self):

        self.tiles = generate_map()

    def get_tile(self, x, y):

        if y < 0 or y >= len(self.tiles):
            return None

        if x < 0 or x >= len(self.tiles[0]):
            return None

        return self.tiles[y][x]