import pygame
from script.entity import Player
from script.tilemap import Tilemap
from script.clouds import Clouds

class MainGame:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.display = self.gameManager.display

        self.movement = [False, False]

        self.clouds = Clouds(self.gameManager.assets["clouds"], count=16)

        self.player = Player(self.gameManager, (100, 50), (30, 42))

        self.tilemap = Tilemap(self.gameManager)

        self.scroll = [0, 0]

    def run(self):
        self.display.blit(pygame.transform.scale(self.gameManager.assets["background"], self.display.get_size()), (0, 0))

        # MOVING THE CAMERA
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)

        self.tilemap.render(self.display, offset=render_scroll)

        self.player.update(self.tilemap, ((self.movement[1] - self.movement[0])*3, 0))
        self.player.render(self.display, offset=render_scroll)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gameManager.changeState("main_menu")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_x:
                    self.player.set_action("prejump")
                    self.player.velocity[1] = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))