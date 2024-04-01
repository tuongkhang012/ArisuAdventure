from .entity import *


class Player(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "player", pos, size)
        self.max_hp = 50
        self.hp = self.max_hp
        self.red_hp = 0

        self.air_time = 0
        self.jump_cnt = 1
        self.wall_slide = False

        # FOR DASHING
        self.dash_cnt = 1
        self.dashingX = 0
        self.dashingY = 0
        self.dashing = 0
        self.dash_gnd = False

        # FOR FIRING
        self.charge = 0
        self.shooting = False
        self.gun_anim = None

        self.invincible_frame = 0

        self.id = 0

    def update(self, tilemap):
        super().update(tilemap)

        if self.invincible_frame:
            self.invincible_frame = max(0, self.invincible_frame - 1)

        entity_rect = self.rect()
        for rect in tilemap.spikes_rects_around(self.pos, True if self.type in TALL else False):
            rect, behaviour = rect
            if entity_rect.colliderect(rect):
                self.hp = max(0, self.hp - 999)
                self.death()

        # DIE IF FALLING TOO FAR
        if self.rect().y > 32 * 30:
            self.scene.dead += 1

        for entity in self.entity_col['right']:
            if entity.type in HARD_OBJECTS and self.collisions['right']:
                entity.dx = self.dx

        for entity in self.entity_col['left']:
            if entity.type in HARD_OBJECTS and self.collisions['left']:
                entity.dx = self.dx

        self.air_time += 1
        if self.collisions['down']:
            if self.air_time > 4:
                if self.dash_cnt:
                    self.set_action("land")
                else:
                    self.set_action("landAlt")
            self.air_time = 0
            self.jump_cnt = 1
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
            elif self.dx != 0:
                if self.dash_cnt:
                    self.set_action("run")
                else:
                    self.set_action("runAlt")
            else:
                if self.dash_cnt:
                    self.set_action("idle")
                else:
                    self.set_action("idleAlt")

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)

        if self.dashing:
            px, py = self.rect().center
            self.scene.particles.append(Particle(self.gameManager, 'afterimage',
                                                 (px, py - 4), p_flip=self.flip))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.3, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.3, 0)

        if self.gun_anim:
            self.gun_anim.update()

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)

        flip_flag = self.flip ^ self.wall_slide
        if not self.shooting:
            surf.blit(pygame.transform.flip(self.gameManager.assets['gun'], flip_flag, False),
                      (self.rect().centerx + 6 - 12 * flip_flag - self.gameManager.assets['gun'].get_width() / 2 -
                       offset[0],
                       self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
        else:
            surf.blit(pygame.transform.flip(self.gun_anim.img(), flip_flag, False),
                      (self.rect().centerx + 6 - 12 * flip_flag - self.gameManager.assets['gun'].get_width() / 2 -
                       offset[0],
                       self.rect().centery + 8 - self.gameManager.assets['gun'].get_height() / 2 - offset[1]))
            if self.gun_anim.done:
                if self.charge >= 30:
                    self.scene.player_projectiles.append(
                        [[self.rect().centerx + 32 - 40 * flip_flag - self.gameManager.assets['gun'].get_width() / 2,
                          self.rect().centery - self.gameManager.assets['charged_bullet'].get_height()/2 + 12 - self.gameManager.assets['gun'].get_height() / 2],
                         [4 - 8 * flip_flag, 0], 0, self.gameManager.assets['charged_bullet'], 20])
                    self.charge = 0
                else:
                    self.scene.player_projectiles.append(
                        [[self.rect().centerx + 32 - 40 * flip_flag - self.gameManager.assets['gun'].get_width() / 2,
                          self.rect().centery - self.gameManager.assets['ally_bullet'].get_height()/2 + 12 - self.gameManager.assets['gun'].get_height() / 2],
                         [4 - 8 * flip_flag, 0], 0, self.gameManager.assets['ally_bullet'], 5])
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
                self.velocity[1] = -5
                self.jump_cnt = max(0, self.jump_cnt - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -5
                self.velocity[1] = -5
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
            self.scene.screenshake = max(8, self.scene.screenshake)
            self.set_action("dash")
            if self.collisions['down']:
                self.dashing = 4
            else:
                self.dashing = 9
            self.velocity = [0,0]
            dir = [keys[3] - keys[2], keys[1] - keys[0]]
            if dir[0] == 0 and dir[1] == 0:
                dir = [1, 0]
            dir = list(map(lambda x: x / math.sqrt(dir[0] ** 2 + dir[1] ** 2), dir))
            self.velocity = list(map(lambda x: x * 5, dir))
            self.dash_cnt = max(0, self.dash_cnt - 1)

    def shoot(self):
        if not self.shooting:
            self.gun_anim = self.gameManager.assets['shooting'].copy()
            self.shooting = True

    def reset(self):
        self.hp = self.max_hp
        self.red_hp = 0
        self.air_time = 0
        self.jump_cnt = 1
        self.wall_slide = False
        self.velocity = [0, 0]

        # FOR DASHING
        self.dash_cnt = 1
        self.dashingX = 0
        self.dashingY = 0
        self.dashing = 0
        self.dash_gnd = False

        # FOR FIRING
        self.charge = 0
        self.shooting = False

    def death(self):
        if self.hp <= 0:
            self.scene.dead += 1
            self.scene.screenshake = max(16, self.scene.screenshake)
            for i in range(30):
                angle = (i / 30) * math.pi * 2
                self.scene.particles.append(Particle(self.gameManager, "dead", self.rect().center,
                                                     velocity=[math.cos(angle) * 2,
                                                               math.sin(angle) * 2],
                                                     frame=0))

    def gravity(self):
        if not self.dashing:
            self.velocity[1] = min(5, self.velocity[1] + 0.3)
