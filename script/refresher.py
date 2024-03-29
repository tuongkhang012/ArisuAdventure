import pygame
import random
import math
from script.spark import Spark


class Refresher:
    def __init__(self, gameManager, pos, size, scene):
        self.gameManager = gameManager
        self.scene = scene
        self.pos = list(pos)
        self.size = size
        self.action = ""
        self.set_action("idle")

        self.timer = -1

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap):
        if self.timer > 0:
            self.timer = max(0, self.timer - 1)

        if self.scene.player.rect().colliderect(self.rect()) and self.action == "idle":
            if self.scene.player.dash_cnt == 0:
                self.scene.player.dash_cnt = 1
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.scene.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                self.set_action("used")
                self.timer = 120

        if self.timer == 0:
            self.timer = -1
            self.set_action("idle")

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        #TAKE EACH FRAME FROM THE ANIMATION AND BLIT IT
        surf.blit(pygame.transform.flip(self.animation.img(), False, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.gameManager.assets["refresher/" + self.action].copy()
