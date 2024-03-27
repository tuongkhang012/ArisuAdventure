from .entity import *


class Enemy(PhysicsEntity):
    def __init__(self, gameManager, pos, size):
        super().__init__(gameManager, "enemy", pos, size)

        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            self.set_action("run")
            movement = (movement[0] - 0.5 if self.flip else movement[0] + 0.5, movement[1])
            self.walking = max(0, self.walking - 1)
        elif random.random() < 0.01:
            self.set_action("idle")
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)