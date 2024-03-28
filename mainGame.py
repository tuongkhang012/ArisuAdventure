import pygame
import random
import math
import os

from script.clouds import Clouds
from script.player import Player
from script.enemy import Enemy
from script.particle import Particle
from script.tilemap import Tilemap
from script.spark import Spark


class MainGame:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.display = self.gameManager.display

        self.movement = [False, False]
        self.pressing = [False, False, False, False]  # UP, DOWN, LEFT, RIGHT

        self.clouds = Clouds(self.gameManager.assets["clouds"], count=16)

        self.player = Player(self.gameManager, (0, 0), (30, 42), self)

        self.tilemap = Tilemap(self.gameManager)

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load(f"./levels/{map_id}.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('willows', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 124, 156))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self.gameManager, spawner['pos'], (30, 42), self))

        self.projectiles = []
        self.player_projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [self.player.rect().centerx - self.display.get_width() / 2,
                       self.player.rect().centery - self.display.get_height() / 2]
        self.dead = 0
        self.transition = -30

        self.screenshake = 0

    def run(self):
        self.display.blit(pygame.transform.scale(self.gameManager.assets["background"], self.display.get_size()),
                          (0, 0))

        self.screenshake = max(0, self.screenshake - 1)

        if not len(self.enemies):
            self.transition += 1
            if self.transition > 30:
                self.level = min(self.level + 1, len(os.listdir('levels')) - 1)
                self.load_level(self.level)
        if self.transition < 0:
            self.transition += 1

        if self.dead:
            self.dead += 1
            if self.dead >= 10:
                self.transition = min(30, self.transition + 1)
            if self.dead > 40:
                self.player.reset()
                self.load_level(self.level)

        # MOVING THE CAMERA
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        for rect in self.leaf_spawners:
            # RANDOM CHANCE
            if random.random() * 49999 < rect.width * rect.height:
                pos = (rect.x + random.random() * rect.width, (rect.y + 40) + random.random() * (rect.height - 40))
                self.particles.append(
                    Particle(self.gameManager, "leaf", pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

        self.clouds.update()
        self.clouds.render(self.display, offset=render_scroll)

        self.tilemap.render(self.display, offset=render_scroll)

        pygame.draw.circle(self.display, (255, 255, 255), (0, 0), 5)

        # SPAWNING ENEMIES
        for enemy in self.enemies.copy():
            enemy.update(self.tilemap, (0, 0))
            enemy.render(self.display, offset=render_scroll)

        # SPAWNING PARTICLES
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

        if not self.dead:
            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * 3, 0))
            self.player.render(self.display, offset=render_scroll)

        # [(x,y), direction, timer] SPAWNING BULLETS
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            img = self.gameManager.assets['bullet']
            if projectile[1] < 0:
                img = pygame.transform.flip(img, True, False)
            self.display.blit(img,
                              (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                               projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(projectile[0],
                                             random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                             2 + random.random()))
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            elif not self.player.dashing:
                if self.player.rect().collidepoint(projectile[0]):
                    self.projectiles.remove(projectile)
                    self.dead += 1
                    self.screenshake = max(16, self.screenshake)
                    for i in range(30):
                        angle = (i/30) * math.pi * 2
                        self.particles.append(Particle(self.gameManager, "dead", self.player.rect().center,
                                                       velocity=[math.cos(angle) * 2,
                                                                 math.sin(angle) * 2],
                                                       frame=0))

        # SPAWNING PLAYER BULLET
        for projectile in self.player_projectiles.copy():
            projectile[0][0] += projectile[1]
            projectile[2] += 1
            img = self.gameManager.assets['bullet']
            if projectile[1] < 0:
                img = pygame.transform.flip(img, True, False)
            self.display.blit(img,
                              (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                               projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.player_projectiles.remove(projectile)
            elif projectile[2] > 360:
                self.player_projectiles.remove(projectile)
            else:
                for enemy in self.enemies.copy():
                    if enemy.rect().collidepoint(projectile[0]):
                        enemy.death()
                        self.player_projectiles.remove(projectile)
                        break

        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(self.display, offset=render_scroll)
            if kill:
                self.sparks.remove(spark)

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
                if event.key == pygame.K_c:
                    self.player.charge += 1
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
                if event.key == pygame.K_c:
                    self.player.shoot()
                    self.player.charge = 0

        if self.transition:
            transition_surf = pygame.Surface(self.display.get_size())
            pygame.draw.circle(transition_surf, (255,255,255), (self.display.get_width()//2, self.display.get_height()//2), (30 - abs(self.transition)) * 12)
            transition_surf.set_colorkey((255,255,255))
            self.display.blit(transition_surf, (0,0))

        screenshake_offset = (random.random() * self.screenshake - self.screenshake/2, random.random() * self.screenshake - self.screenshake/2)
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)