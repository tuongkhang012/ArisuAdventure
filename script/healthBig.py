import pygame

from script.entity import PhysicsEntity


class HealBig(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "healthSmol", pos, size)

        self.anim_offset = (0, 0)
        self.hp_heal = 20

    def update(self, tilemap):
        self.set_action("idle")

        super().update(tilemap)

        entity_rect = self.rect()
        if self.scene.player.rect().colliderect(entity_rect):
            self.scene.player.red_hp = max(0, self.scene.player.red_hp - self.hp_heal)
            self.scene.player.hp = min(self.scene.player.max_hp, self.scene.player.hp + self.hp_heal)
            self.scene.items.remove(self)

        self.flip = False

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)