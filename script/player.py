from .entity import *


class Player(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, "player", pos, size)
        self.scene = scene
        self.air_time = 0
        self.jump_cnt = 1
        self.wall_slide = False

        # FOR DASHING
        self.dash_cnt = 1
        self.dashingX = 0
        self.dashingY = 0
        self.dashing = 0
        self.dash_gnd = False

        #FOR FIRING
        self.charge = 0
        self.shooting = False
        self.gun_anim = None

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        # DIE IF FALLING TOO FAR
        if self.rect().y > 32*30:
            self.scene.dead += 1

        self.air_time += 1
        if self.collisions['down']:
            if self.air_time > 4:
                if self.dash_cnt:
                    self.set_action("land")
                else:
                    self.set_action("landAlt")
            self.air_time = 0
            self.jump_cnt = 1
            self.dashingY = 0
            if not self.dash_gnd:
                self.dashingX = 0
                self.dashing = 0
            self.dash_cnt = 1

        if self.collisions['up'] or self.collisions['right'] or self.collisions['left']:
            self.dashingY = 1
            self.dashingX = 1
            self.dashing = 0

        self.wall_slide = False
        if (self.collisions['left'] or self.collisions['right']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(2, self.velocity[1])
            if self.collisions['left']:
                self.flip = True
            else:
                self.flip = False
            if self.dash_cnt:
                self.set_action("wallslide")
            else:
                self.set_action("wallslideAlt")

        if not self.wall_slide:
            if self.velocity[1] < 0:
                if self.dash_cnt:
                    self.set_action("jump")
                else:
                    self.set_action("jumpAlt")

            if self.velocity[1] > 0 and self.air_time > 4:
                if self.dash_cnt:
                    self.set_action("fall")
                else:
                    self.set_action("fallAlt")
            elif movement[0] != 0:
                if self.dash_cnt:
                    self.set_action("run")
                else:
                    self.set_action("runAlt")
            else:
                if self.dash_cnt:
                    self.set_action("idle")
                else:
                    self.set_action("idleAlt")

        if self.dashingX > 0:
            self.dashingX = max(0, self.dashingX - 1)
        if self.dashingX < 0:
            self.dashingX = min(0, self.dashingX + 1)
        if self.dashingY > 0:
            self.dashingY = max(0, self.dashingY - 1)
        if self.dashingY < 0:
            self.dashingY = min(0, self.dashingY + 1)
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)

        if self.dashing > 10:
            px, py = self.rect().center
            self.scene.particles.append(Particle(self.gameManager, 'afterimage',
                                                 (px, py-4), p_flip=self.flip))

        if abs(self.dashingX) in range(1,3):
            self.velocity[0] *= 0.3
        if abs(self.dashingY) in range(1,3):
            self.velocity[1] += 0.3

        if not self.dashingX:
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.3, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.3, 0)
        else:
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.5, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.5, 0)

        if self.gun_anim:
            print("A")
            self.gun_anim.update()
        print(self.shooting)

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

        flip_flag = self.flip ^ self.wall_slide
        if not self.shooting:
            surf.blit(pygame.transform.flip(self.gameManager.assets['gun'], flip_flag, False),
                      (self.rect().centerx + 6 - 12 * flip_flag - self.gameManager.assets['gun'].get_width() / 2 - offset[0],
                       self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
        else:
            surf.blit(pygame.transform.flip(self.gun_anim.img(), flip_flag, False),
                      (self.rect().centerx + 6 - 12 * flip_flag - self.gameManager.assets['gun'].get_width() / 2 -
                       offset[0],
                       self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
            if self.gun_anim.done:
                self.scene.player_projectiles.append(
                    [[self.rect().centerx + 32 - 40 * flip_flag - self.gameManager.assets['gun'].get_width() / 2,
                      self.rect().centery + 12 - self.gameManager.assets['gun'].get_height() / 2],
                     4 - 8 * flip_flag, 0])
                self.shooting = False

    # THE BOOLEAN RETURN IS USED TO CHECK IF THE PLAYER JUMPED
    def jump(self):
        if self.wall_slide:
            if self.dash_cnt:
                self.set_action("prejump")
            else:
                self.set_action("prejumpAlt")
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 5
                self.velocity[1] = -4
                self.jump_cnt = max(0, self.jump_cnt - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -5
                self.velocity[1] = -4
                self.jump_cnt = max(0, self.jump_cnt - 1)
                return True

        elif self.jump_cnt:
            if self.dash_cnt:
                self.set_action("prejump")
            else:
                self.set_action("prejumpAlt")
            self.velocity[1] = -6
            self.jump_cnt -= 1
            return True

        return False

    def dash(self, keys):
        if self.dash_cnt:
            self.set_action("dash")
            if self.collisions['down']:
                self.dash_gnd = True
            if keys[0]:
                self.dashingY = -30
                self.velocity[1] = -6
            if keys[1]:
                self.dashingY = 30
                self.velocity[1] = 6
            if keys[2]:
                self.dashingX = -30
                self.velocity[0] = -6
            if keys[3]:
                self.dashingX = 30
                self.velocity[0] = 6
            self.dashing = 30
            self.dash_cnt = max(0, self.dash_cnt - 1)

    def shoot(self):
        if not self.shooting:
            self.gun_anim = self.gameManager.assets['shooting'].copy()
            self.shooting = True

    def reset(self):
        self.air_time = 0
        self.jump_cnt = 1
        self.wall_slide = False
        self.velocity = [0,0]

        # FOR DASHING
        self.dash_cnt = 1
        self.dashingX = 0
        self.dashingY = 0
        self.dashing = 0
        self.dash_gnd = False

        # FOR FIRING
        self.charge = 0
        self.shooting = False
