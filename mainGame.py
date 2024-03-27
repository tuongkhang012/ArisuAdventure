import pygame
import random
import math

from script.clouds import Clouds
from script.player import Player
from script.enemy import Enemy
from script.particle import Particle
from script.tilemap import Tilemap


class MainGame:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.display = self.gameManager.display

        self.movement = [False, False]
        self.pressing = [False, False, False, False] # UP, DOWN, LEFT, RIGHT

        self.clouds = Clouds(self.gameManager.assets["clouds"], count=16)

        self.player = Player(self.gameManager, (0, 0), (30, 42), self)

        self.tilemap = Tilemap(self.gameManager)
        self.tilemap.load("./levels/map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('willows', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 124, 156))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self.gameManager, spawner['pos'], (30, 42)))

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

        for enemy in self.enemies.copy():
            print("ENEMY")
            enemy.update(self.tilemap, (0, 0))
            enemy.render(self.display, offset=render_scroll)

        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

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
                    self.pressing[2] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                    self.pressing[3] = True
                if event.key == pygame.K_UP:
                    self.pressing[0] = True
                if event.key == pygame.K_DOWN:
                    self.pressing[1] = True
                if event.key == pygame.K_x:
                    self.player.jump()
                if event.key == pygame.K_z:
                    self.player.dash(self.pressing)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                    self.pressing[2] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False
                    self.pressing[3] = False
                if event.key == pygame.K_UP:
                    self.pressing[0] = False
                if event.key == pygame.K_DOWN:
                    self.pressing[1] = False

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))