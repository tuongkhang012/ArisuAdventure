import pygame

from .entity import *
import random


from script.spark import Spark

# 270, 285, 300, 315, 330, 30, 45, 60, 75, 90
ANGLES = [3*math.pi/2, 19*math.pi/12, 5*math.pi/3, 7*math.pi/4, 11*math.pi/6, math.pi/6, math.pi/4, math.pi/3, 5*math.pi/12, math.pi/2]

class NeruDed(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "neru_ded", pos, size)

        self.anim_offset = [0, 0]

        self.set_action("idle")

    def update(self, tilemap):
        super().update(tilemap)
