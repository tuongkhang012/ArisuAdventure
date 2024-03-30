import pygame
import random
import math
from .spark import Spark


class Checkpoint:
    def __init__(self, gameManager, pos, size, scene, id):
        self.gameManager = gameManager
        self.scene = scene
        self.pos = list(pos)
        self.size = size
        self.action = ""
        self.id = id
        self.set_action("untouched")

        self.timer = -1

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap):
        if self.scene.player.rect().colliderect(self.rect()):
            if self.action == "untouched":
                self.set_action("burn")
                self.scene.player.id = self.id
                for i in range(15):
                    angle = random.random() * - math.pi
                    self.scene.sparks.append(Spark(self.rect().midbottom, angle, 0.5 + random.random(), (233, 250, 0, 0)))
                    self.scene.sparks.append(Spark(self.rect().midbottom, angle, 2 + random.random(), (255, 136, 0)))
            self.scene.player.hp = self.scene.player.max_hp

        if self.action == "burn" and self.animation.done:
            self.set_action("idle")

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        #TAKE EACH FRAME FROM THE ANIMATION AND BLIT IT
        surf.blit(pygame.transform.flip(self.animation.img(), False, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.gameManager.assets["checkpoint/" + self.action].copy()