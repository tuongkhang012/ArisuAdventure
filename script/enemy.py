from .entity import *

from script.spark import Spark

class Enemy(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, "enemy", pos, size)

        self.scene = scene
        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-29 if self.flip else 29), self.pos[1] + 16 + 42)):
                if self.collisions['left'] or self.collisions['right']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else movement[0] + 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                # Calculate the distance between the enemy and the player (PLAYER - ENEMY)
                dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
                # if the distance (for y) is less than 32 pixels
                if abs(dis[1]) < 64:
                    # if turned left, and player is on the left
                    if self.flip and dis[0] < 0:
                        self.scene.projectiles.append(
                            [[self.rect().centerx - 4 - self.gameManager.assets['gun'].get_width() / 2,
                             self.rect().centery + 12 - self.gameManager.assets['gun'].get_height() / 2],
                             -4, 0])
                        for i in range(4):
                            self.scene.sparks.append(Spark(self.scene.projectiles[-1][0],
                                                           random.random() - 0.5 + math.pi, 2 + random.random()))
                            # PLUS MATH.PI TO MAKE THE BULLET SPIN LEFT

                    # if turned right, and player is on the right
                    if not self.flip and dis[0] > 0:
                        self.scene.projectiles.append(
                            [[self.rect().centerx + 32 - self.gameManager.assets['gun'].get_width() / 2,
                             self.rect().centery + 12 - self.gameManager.assets['gun'].get_height() / 2],
                             4, 0])
                        for i in range(4):
                            self.scene.sparks.append(Spark(self.scene.projectiles[-1][0],
                                                           random.random() - 0.5, 2 + random.random()))
                            # PLUS 0 TO MAKE THE BULLET SPIN RIGHT

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        if movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        super().update(tilemap, movement)

    def death(self):
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

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

        surf.blit(pygame.transform.flip(self.gameManager.assets['gun'], self.flip, False),
                  (self.rect().centerx + 6 - 12*self.flip - self.gameManager.assets['gun'].get_width() / 2 - offset[0],
                   self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
