import pygame
import random
import math

from script.clouds import Clouds
from script.entity import Player
from script.particle import Particle
from script.tilemap import Tilemap


class MainGame:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.display = self.gameManager.display

        self.movement = [False, False]

        self.clouds = Clouds(self.gameManager.assets["clouds"], count=16)

        self.player = Player(self.gameManager, (0, 0), (30, 42))

        self.tilemap = Tilemap(self.gameManager)
        self.tilemap.load("./levels/map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('willows', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 124, 156))

        self.particles = []

        self.scroll = [self.player.rect().centerx - self.display.get_width() / 2, self.player.rect().centery - self.display.get_height() / 2]

    def run(self):
        self.display.blit(pygame.transform.scale(self.gameManager.assets["background"], self.display.get_size()), (0, 0))

        # MOVING THE CAMERA

        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        for rect in self.leaf_spawners:
            #RANDOM CHANCE
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, (rect.y + 40) + random.random() * (rect.height - 40))
                self.particles.append(Particle(self.gameManager, "leaf", pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)

        self.tilemap.render(self.display, offset=render_scroll)

        self.player.update(self.tilemap, ((self.movement[1] - self.movement[0])*3, 0))
        self.player.render(self.display, offset=render_scroll)

        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

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
                    self.player.velocity[1] = -7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))