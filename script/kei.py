import pygame
import random
import math
from .spark import Spark

class Kei:
    def __init__(self, gameManager, scene, level, id, pos, size):
        self.gameManager = gameManager
        self.scene = scene
        self.level = level
        self.id = id
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock

        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        if self.scene.player.rect().colliderect(self.rect()):
            self.gameManager.data["kei"].append(str(self.level) + ";" + str(self.id))
            for i in range(30):
                angle = random.random() * math.pi * 2
                self.scene.sparks.append(Spark(self.rect().center, angle, 2 + random.random(), (0, 200, 255)))
            self.scene.keis.remove(self)

    def render(self, surf, offset):
        surf.blit(self.gameManager.assets["kei"], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
