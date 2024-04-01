import pygame

from .entity import *
import random


from script.spark import Spark

# 0, 45, 90, 135, 180, 225, 270, 315
QUAD_ANGLES = [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]
OCT_ANGLES = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]
MOVES = ["smash", "dual_volleyL", "dual_volley_R", "split_bullet", "push_L", "push_R", "homing_bullet"]

class Yuuka(PhysicsEntity):
    def __init__(self, gameManager, pos, size, scene):
        super().__init__(gameManager, scene, "yuuka", pos, size)

        self.name = "Hayase Yuuka"
        self.max_hp = 150
        self.hp = 150
        self.active_radius = 8*32
        self.anim_offset = (0, 0)

        self.topleft = 0
        self.topright = 0
        self.botleft = 0
        self.botright = 0
        self.room_w = 18*32
        self.room_h = 7*32

        self.active = False
        self.invincible = False
        self.teleport = False
        self.volley = False
        self.inAction = False
        self.enrage = False
        self.enrage_attack = False
        self.render_warning = False
        self.hitbox_active = False

        self.waitTimer = 35
        self.smash_wait = 60
        self.volley_wait = 0

        self.choice = ""
        self.previous_choice = ""
        self.count = 0
        self.warning_wait = 60
        self.set_action("idle")

    def update(self, tilemap):
        if self.scene.player.rect().colliderect(self.pos[0] - self.active_radius, self.pos[1] - self.active_radius,
                                                self.active_radius*2, self.active_radius*2) and not self.active:
            self.scene.boss_encounter = True
            self.activate()

        if self.hitbox_active:
            if self.scene.player.rect().colliderect(self.rect()) and not self.scene.player.dashing:
                dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
                if not self.scene.player.invincible_frame:
                    self.scene.player.hurting = True
                    self.scene.player.hp = max(0, self.scene.player.hp - 7)
                    if not self.scene.player.red_hp:
                        self.scene.player.red_hp = 0.6*7
                    self.scene.player.invincible_frame = 30
                if dis[0] < 0:
                    self.scene.player.velocity[0] = -7
                else:
                    self.scene.player.velocity[0] = 7

        self.set_action("idle")

        if self.active and not self.inAction: #and not self.enrage_attack:
            if self.waitTimer >= 10:
                self.waitTimer = max(0, self.waitTimer - 1)
            elif self.waitTimer > 0:
                self.waitTimer = max(0, self.waitTimer - 1)
                self.invincible = True
            else:
                self.inAction = True
                self.deciding()
                if self.choice == "smash":
                    self.smash()
                elif self.choice == "dual_volleyL":
                    self.dual_volleyL()
                elif self.choice == "dual_volley_R":
                    self.dual_volleyR()
                elif self.choice == "split_bullet":
                    self.split_bullet()

                self.waitTimer = 50
        elif self.inAction: #and not self.enrage_attack:
            if self.choice == "smash":
                self.smash()
            elif self.choice == "dual_volleyL":
                self.dual_volleyL()
            elif self.choice == "dual_volley_R":
                self.dual_volleyR()
            elif self.choice == "split_bullet":
                self.split_bullet()

        super().update(tilemap)

    def hit_rect(self):
        return pygame.Rect(self.rect().centerx - 30, self.rect().bottom - 64, 60, 64)

    def render(self, surf, offset=(0, 0)):
        if self.render_warning:
            lpoints = [
                (self.rect().center[0] - offset[0], self.rect().center[1] - offset[1]),
                (self.rect().centerx - math.sin(math.pi / 3) * 60 - offset[0], self.botleft[1] - offset[1]),
                (self.botleft[0] - offset[0], self.botleft[1] - offset[1]),
                (self.topleft[0] - offset[0], self.topleft[1] - offset[1]),
            ]
            rpoints = [
                (self.rect().center[0] - offset[0], self.rect().center[1] - offset[1]),
                (self.rect().centerx + math.sin(math.pi / 3) * 60 - offset[0], self.botleft[1] - offset[1]),
                (self.botright[0] - offset[0], self.botright[1] - offset[1]),
                (self.topright[0] - offset[0], self.topright[1] - offset[1]),
            ]
            pygame.draw.polygon(surf, (255, 0, 0, 50), lpoints)
            pygame.draw.polygon(surf, (255, 0, 0, 50), rpoints)
        if not self.invincible:
            super().render(surf, offset)
            pygame.draw.rect(self.gameManager.display, (255, 255, 255), (self.rect().topleft[0] - offset[0], self.rect().topleft[1] - offset[1], self.size[0], self.size[1]), 1)
            pygame.draw.rect(self.gameManager.display, (0, 255, 0), (
            self.rect().centerx - 30 - offset[0], self.rect().bottom - 64 - offset[1], 60, 64), 1)

    def death(self):
        if self.hp <= 0:
            self.scene.boss_encounter = False
            self.scene.bosses.remove(self)
            self.scene.projectiles.clear()
            self.scene.screenshake = max(32, self.scene.screenshake)
            for i in range(30):
                angle = random.random() * math.pi * 2
                self.scene.sparks.append(Spark(self.rect().topright, angle, 5 + random.random(), (255, 242, 0)))
            for i in range(30):
                angle = random.random() * math.pi * 2
                self.scene.sparks.append(Spark(self.rect().midleft, angle, 5 + random.random(), (255, 242, 0)))
            for i in range(30):
                angle = random.random() * math.pi * 2
                self.scene.sparks.append(Spark(self.rect().midbottom, angle, 5 + random.random(), (255, 242, 0)))
            self.scene.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
            self.scene.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))

    def activate(self):
        self.topleft = (self.pos[0] - 8 * 32, self.pos[1] - 2 * 32)
        self.topright = (self.pos[0] + 10 * 32, self.pos[1] - 2 * 32)
        self.botleft = (self.pos[0] - 8 * 32, self.pos[1] + 5 * 32)
        self.botright = (self.pos[0] + 10 * 32, self.pos[1] + 5 * 32)
        self.active = True

    def EuclideanDistance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    #MOVES = ["smash", "dual_volleyL", "dual_volley_R", "split_bullet", "push_L", "push_R", "homing_bullet"]
    def deciding(self):
        weights_saved = [0.1, 0.15, 0.15, 0.1, 0.15, 0.15, 0.2]
        self.choice = random.choices(MOVES, weights=[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], k=1)[0]
        self.previous_choice = self.choice

    def raging(self):
        self.render_warning = False
        for angle in OCT_ANGLES:
            angle_x = math.sin(angle)*5
            angle_y = math.cos(angle)*5
            self.scene.projectiles.append(
                [[self.rect().centerx - 4,
                  self.rect().centery - self.gameManager.assets['smg_bullet'].get_height() / 2 + 12],
                 [angle_x, angle_y], 0, self.gameManager.assets['smg_bullet'], 1])

        self.volley_wait = 10

        self.count += 1
        if self.count == 15:
            self.inAction = False
            self.volley = False
            self.count = 0
            self.set_action("idle")
            self.invincible = False
            self.enrage_attack = False
            self.hurting = False

    def gravity(self):
        if self.volley:
            super().gravity()

    def smash(self):
        self.invincible = False
        if self.smash_wait >= 15:
            print("LOOMING")
            self.pos[0] = self.scene.player.rect().centerx - self.size[0] / 2
            self.pos[1] = self.scene.player.rect().top - self.size[1] - 30
            self.smash_wait = max(0, self.smash_wait - 1)
        elif self.smash_wait > 0:
            print("PAUSING")
            self.smash_wait = max(0, self.smash_wait - 1)
        else:
            print("SMASHING")
            self.hitbox_active = True
            self.dy = 10
            self.smash_wait = max(0, self.smash_wait - 1)

            if self.collisions['down']:
                print("RESET")
                self.dy = 0
                self.smash_wait = 45

                self.count += 1
                if self.count == 3:
                    self.inAction = False
                    self.hitbox_active = False
                    self.count = 0

    def dual_volleyL(self):
        self.invincible = False

        if self.count == 0:
            print("STANDBY")
            self.pos[0] = self.topleft[0] + 32*2
            self.pos[1] = self.topleft[1] + 32*2
            self.dx = 5
            self.hitbox_active = True
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        if self.volley_wait:
            self.volley_wait = max(0, self.volley_wait - 1)
        else:
            for angle in target_angle:
                bullet_x = math.sin(angle)*7
                bullet_y = math.cos(angle)*7
                self.scene.projectiles.append(
                    [[self.rect().centerx,
                      self.rect().centery],
                     [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 3])
            self.volley_wait = 10


        if self.EuclideanDistance(self.pos, self.topright) < 32*4:
            print("STOP")
            self.dx = 0
            self.inAction = False
            self.hitbox_active = False
            self.count = 0

    def dual_volleyR(self):
        self.invincible = False

        if self.count == 0:
            print("STANDBY")
            self.pos[0] = self.topright[0] - 32*2
            self.pos[1] = self.topright[1] + 32*2
            self.dx = -5
            self.hitbox_active = True
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        if self.volley_wait:
            self.volley_wait = max(0, self.volley_wait - 1)
        else:
            for angle in target_angle:
                bullet_x = math.sin(angle)*7
                bullet_y = math.cos(angle)*7
                self.scene.projectiles.append(
                    [[self.rect().centerx,
                      self.rect().centery],
                     [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 3])
            self.volley_wait = 10


        if self.EuclideanDistance(self.pos, self.topleft) < 32*4:
            print("STOP")
            self.dx = 0
            self.inAction = False
            self.hitbox_active = False
            self.count = 0

    def split_bullet(self):
        self.invincible = False

        if self.count == 0:
            self.pos[0] = self.topleft[0] + self.room_w/2 - self.rect().width/2
            self.pos[1] = self.topleft[1] + self.room_h/2 - self.rect().height/2
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        for angle in target_angle:
            bullet_x = math.sin(angle)*5
            bullet_y = math.cos(angle)*5
            self.scene.special_bullets.append(
                [[self.rect().centerx,
                  self.rect().centery],
                 [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 7, "split"])

        self.inAction = False
        self.count = 0

