FOW_UNSEEN = 0
FOW_EXPLORED = 1
FOW_VISIBLE = 2


class FOWSystem:

    def __init__(
        self,
        width,
        height
    ):

        self.width = width
        self.height = height

        self.tiles = []

        for y in range(height):

            row = []

            for x in range(width):

                row.append(FOW_UNSEEN)

            self.tiles.append(row)

    # =====================================================
    # RESET CURRENT VISIBILITY
    # =====================================================

    def clear_visible(self):

        for y in range(self.height):

            for x in range(self.width):

                if self.tiles[y][x] == FOW_VISIBLE:

                    self.tiles[y][x] = FOW_EXPLORED

    # =====================================================
    # REVEAL TILE
    # =====================================================

    def reveal_tile(
        self,
        x,
        y
    ):

        if (
            x < 0 or
            y < 0 or
            x >= self.width or
            y >= self.height
        ):
            return

        self.tiles[y][x] = FOW_VISIBLE

    # =====================================================
    # QUERY
    # =====================================================

    def get_visibility(
        self,
        x,
        y
    ):

        if (
            x < 0 or
            y < 0 or
            x >= self.width or
            y >= self.height
        ):
            return FOW_UNSEEN

        return self.tiles[y][x]

    def is_visible(
        self,
        x,
        y
    ):

        return (
            self.get_visibility(x, y)
            == FOW_VISIBLE
        )

    def is_explored(
        self,
        x,
        y
    ):

        return (
            self.get_visibility(x, y)
            != FOW_UNSEEN
        )