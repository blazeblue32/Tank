import pygame
import math

from core.constants import *
from entities.tank_base import TankBase

class EnemyTank(TankBase):

    def __init__(
        self,
        tilemap,
        x,
        y
    ):

        super().__init__(tilemap)

        self.x = x
        self.y = y

        self.tile_x = x // TILE_SIZE
        self.tile_y = y // TILE_SIZE

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        pass
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, surface, camera):

        super().draw(surface, camera)

        