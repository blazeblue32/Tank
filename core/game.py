import pygame

from core.constants import *
from core.camera import Camera

from world.tilemap import TileMap
from entities.tank import Tank
from entities.enemy_tank import EnemyTank
from rendering.renderer import Renderer
from systems.movement import update_input_state

class Game:

    def __init__(self):

        pygame.init()
        
        update_input_state()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        pygame.display.set_caption("Steel Thunder 800")

        self.clock = pygame.time.Clock()

        self.running = True

        # =================================================
        # WORLD
        # =================================================

        self.tilemap = TileMap()

        # =================================================
        # PLAYER
        # =================================================
     
        self.player = Tank(self.tilemap)

        # =================================================
        # ENEMIES
        # =================================================

        self.enemy_tanks = [

            EnemyTank(
                self.player.x + 220,
                self.player.y + 120
            ),

            EnemyTank(
                self.player.x - 180,
                self.player.y - 140
            )
        ]
        
        # =================================================
        # CAMERA
        # =================================================

        self.camera = Camera()

        # =================================================
        # RENDERER
        # =================================================

        self.renderer = Renderer()

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()

            self.update(dt)

            self.draw()

        pygame.quit()

    # =====================================================
    # EVENTS
    # =====================================================

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        self.player.update(dt)

        for enemy in self.enemy_tanks:
            enemy.update(dt)

        self.camera.update(
            self.player.x,
            self.player.y
        )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        self.screen.fill(BLACK)

        self.renderer.draw_map(
            self.screen,
            self.tilemap,
            self.camera
        )

        self.player.draw(
            self.screen,
            self.camera
        )
        
        for enemy in self.enemy_tanks:
            enemy.draw(
                self.screen,
                self.camera
            )

        pygame.display.flip()