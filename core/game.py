import pygame

from core.constants import *
from core.camera import Camera

from world.tilemap import TileMap
from entities.player_tank import PlayerTank
from entities.enemy_tank import EnemyTank
from rendering.renderer import Renderer
from systems.movement import update_input_state
from systems.visibility import can_see, can_see_tile
from systems.awareness import AwarenessSystem
from systems.fow import FOWSystem

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
     
        self.player = PlayerTank(self.tilemap)

        # =================================================
        # ENEMIES
        # =================================================

        self.enemy_tanks = [

            EnemyTank(
                self.tilemap,
                self.player.x + 220,
                self.player.y + 120
            ),

            EnemyTank(
                self.tilemap,
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
        
        # =================================================
        # AWARENESS
        # =================================================

        self.player_awareness = AwarenessSystem()
        
        # =================================================
        # FOG OF WAR
        # =================================================

        self.fow = FOWSystem(
            MAP_WIDTH,
            MAP_HEIGHT
        )

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

        self.player.update(
            dt,
            self.enemy_tanks
        )

        for enemy in self.enemy_tanks:
            enemy.update(
                dt,
                self.player
            )
            
        current_time = (
            pygame.time.get_ticks() / 1000.0
        )

        for enemy in self.enemy_tanks:

            visible = can_see(
                self.player,
                enemy
            )

            # =============================================
            # FOW AUTHORITATIVE VISIBILITY
            # =============================================

            visible = (

                visible and

                self.fow.is_visible(
                    enemy.tile_x,
                    enemy.tile_y
                )
            )

            self.player_awareness.update_contact(
                enemy,
                visible,
                current_time
            )

        self.player_awareness.cleanup_contacts(
            current_time
        )

        self.update_fow()

        self.camera.update(
            self.player.x,
            self.player.y
        )

    # =====================================================
    # UPDATE FOG OF WAR
    # =====================================================

    def update_fow(self):

        self.fow.clear_visible()
        
        self.fow.reveal_tile(
            self.player.tile_x,
            self.player.tile_y
        )

        reveal_radius = 14

        px = self.player.tile_x
        py = self.player.tile_y

        for y in range(MAP_HEIGHT):

            for x in range(MAP_WIDTH):

                dx = x - px
                dy = y - py

                distance = (
                    dx * dx +
                    dy * dy
                )

                if distance > (
                    self.player.view_range *
                    self.player.view_range
                ):
                    continue

                if can_see_tile(
                    self.player,
                    x,
                    y
                ):

                    self.fow.reveal_tile(
                        x,
                        y
                    )
    
    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        self.screen.fill(BLACK)

        self.renderer.draw_map(
            self.screen,
            self.tilemap,
            self.camera,
            self.fow
        )

        # =================================================
        # PROJECTILES + EFFECTS
        # =================================================

        all_tanks = (
            [self.player] +
            self.enemy_tanks
        )

        for tank in all_tanks:

            for projectile in tank.projectiles:
                projectile.draw(
                    self.screen,
                    self.camera
                )

            for particle in tank.particles:
                particle.draw(
                    self.screen,
                    self.camera
                )
        
        # =================================================
        # OBJECTS
        # =================================================        
        
        self.player.draw(
            self.screen,
            self.camera
        )
        
        for enemy in self.enemy_tanks:

            # =============================================
            # CURRENTLY VISIBLE
            # =============================================

            if self.player_awareness.target_visible(
                enemy
            ):

                enemy.draw(
                    self.screen,
                    self.camera
                )

            # =============================================
            # LAST KNOWN POSITION
            # =============================================

            elif self.player_awareness.knows_target(
                enemy
            ):

                last_known = (
                    self.player_awareness
                    .get_last_known_position(enemy)
                )

                if last_known:

                    lx, ly = last_known

                    screen_x = (
                        lx +
                        TILE_SIZE // 2 -
                        self.camera.x
                    )

                    screen_y = (
                        ly +
                        TILE_SIZE // 2 -
                        self.camera.y
                    )

                    pygame.draw.circle(
                        self.screen,
                        (70, 70, 70),
                        (
                            int(screen_x),
                            int(screen_y)
                        ),
                        12,
                        2
                    )

        pygame.display.flip()