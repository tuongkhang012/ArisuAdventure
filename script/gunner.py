from .entity import *

from script.spark import Spark
from .healthDrop import HealthDrop


class Gunner(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "gunner", pos, size)

        self.hp = 10
        self.walking = 0

    def update(self, tilemap):
        if self.scene.player.rect().collidepoint((self.rect().centerx, self.pos[1] - 2)):
            self.hp -= 90
            self.scene.player.velocity[1] = -5
            self.scene.player.dash_cnt = min(1, self.scene.player.dash_cnt + 1)
            self.death()
        elif self.scene.player.rect().colliderect(self.rect()):
            dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
            self.scene.player.hurting = True
            self.scene.player.hp = max(0, self.scene.player.hp - 2)
            self.scene.player.red_hp = 0
            self.scene.player.death()
            if dis[0] < 0:
                self.scene.player.velocity[0] = -5
            else:
                self.scene.player.velocity[0] = 5

        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-29 if self.flip else 29), self.pos[1] + 16 + 42)):
                if self.collisions['left'] or self.collisions['right']:
                    self.dx = 0
                    self.flip = not self.flip
                else:
                    self.dx = -0.5 if self.flip else 0.5
                    self.dy = self.dy
            else:
                self.dx = 0
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                self.dx = 0
                self.dy = 0
                # Calculate the distance between the enemy and the player (PLAYER - ENEMY)
                dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
                # if the distance (for y) is less than 32 pixels
                if abs(dis[1]) < 64:
                    # if turned left, and player is on the left
                    if self.flip and dis[0] < 0:
                        self.scene.projectiles.append(
                            [[self.rect().centerx - 4 - self.gameManager.assets['gun'].get_width() / 2,
                              self.rect().centery - self.gameManager.assets['enemy_bullet'].get_height()/2 + 12 - self.gameManager.assets['gun'].get_height() / 2],
                             [-4, 0], 0, self.gameManager.assets['enemy_bullet'], 5])
                        for i in range(4):
                            self.scene.sparks.append(Spark(self.scene.projectiles[-1][0],
                                                           random.random() - 0.5 + math.pi, 2 + random.random()))
                            # PLUS MATH.PI TO MAKE THE BULLET SPIN LEFT

                    # if turned right, and player is on the right
                    if not self.flip and dis[0] > 0:
                        self.scene.projectiles.append(
                            [[self.rect().centerx + 32 - self.gameManager.assets['gun'].get_width() / 2,
                              self.rect().centery - self.gameManager.assets['enemy_bullet'].get_height()/2 + 12 - self.gameManager.assets['gun'].get_height() / 2],
                             [4, 0], 0, self.gameManager.assets['enemy_bullet'], 5])
                        for i in range(4):
                            self.scene.sparks.append(Spark(self.scene.projectiles[-1][0],
                                                           random.random() - 0.5, 2 + random.random()))
                            # PLUS 0 TO MAKE THE BULLET SPIN RIGHT

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        if self.dx != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        super().update(tilemap)

    def death(self):
        if self.hp <= 0:
            self.scene.enemies.remove(self)
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
            drop = random.choices([0, 1, 2], weights=[0.75, 0.1, 0.05], k=1)[0]
            if drop == 1:
                self.scene.items.append(HealthDrop("healthSmol", self.gameManager, self.rect().center, (6,6), self.scene))
            elif drop == 2:
                self.scene.items.append(HealthDrop("healthBig", self.gameManager, self.rect().center, (10,10), self.scene))

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

        surf.blit(pygame.transform.flip(self.gameManager.assets['gun'], self.flip, False),
                  (
                  self.rect().centerx + 6 - 12 * self.flip - self.gameManager.assets['gun'].get_width() / 2 - offset[0],
                  self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
