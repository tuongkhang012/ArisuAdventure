import pygame

from .entity import PhysicsEntity

class Box(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "box", pos, size)

        self.anim_offset = (0, 0)

    def update(self, tilemap):
        self.set_action("idle")

        super().update(tilemap)

        for entity in self.entity_col['right']:
            if entity.dx < 0:
                print("A")
                print(self.dx)
                self.dx = entity.dx

        for entity in self.entity_col['left']:
            if entity.dx > 0:
                print("B")
                self.dx = entity.dx

        self.flip = False
        self.dx = max(0, self.dx-0.3)

    def check_entity(self, pos, entity):
        if entity.rect().collidepoint(pos):
            return entity

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)