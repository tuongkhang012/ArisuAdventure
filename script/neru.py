from .entity import *

from script.spark import Spark


class Neru(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "neru", pos, size)

        self.max_hp = 100
        self.hp = 100
        self.active_radius = 32*11

        self.active = False
        self.invincible = False

    def update(self, tilemap):
        if self.scene.player.rect().colliderect(self.pos[0] - self.active_radius, self.pos[1] - self.active_radius,
                                                self.active_radius*2, self.active_radius*2):
            self.scene.boss_encounter = True
            self.active = True

        if self.scene.player.rect().colliderect(self.rect()):
            dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
            self.scene.player.hurting = True
            self.scene.player.hp = max(0, self.scene.player.hp - 2)
            self.scene.player.red_hp = 0
            self.scene.player.death()
            if dis[0] < 0:
                self.scene.player.velocity[0] = -5
            else:
                self.scene.player.velocity[0] = 5

        self.set_action("idle")

        if self.active:
            # APPEAR
            # 3 CHOICES
            # DASH
            # SHOOT DIAGONALS
            # RAGE -> SHOOT
            # DISAPPEAR
            pass

        super().update(tilemap)

    def death(self):
        if self.hp <= 0:
            self.scene.boss_encounter = False
            self.scene.bosses.remove(self)
            self.scene.screenshake = max(16, self.scene.screenshake)
            for i in range(30):
                angle = random.random() * math.pi * 2
                speed = random.random() * 5
                self.scene.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                self.scene.particles.append(Particle(self.gameManager, "particle", self.rect().center,
                                                     velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                               math.sin(angle + math.pi) * speed * 0.5],
                                                     frame=random.randint(0, 7)))
            self.scene.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
            self.scene.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

    def disappear(self):
        pass

