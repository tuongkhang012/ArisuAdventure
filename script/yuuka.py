import pygame

from .entity import *
import random


from script.spark import Spark

# 0, 45, 90, 135, 180, 225, 270, 315
QUAD_ANGLES = [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]
OCT_ANGLES = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]
MOVES = ["smash", "dual_volleyL", "dual_volley_R", "split_bullet", "push_L", "push_R"]

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
        self.inAction = False
        self.enrage = False
        self.enrage_attack = False
        self.render_warning = False
        self.hitbox_active = False

        self.waitTimer = 35
        self.smash_wait = 60
        self.volley_wait = 0
        self.first_phaseTimer = 60
        self.angle = 180

        self.choice = ""
        self.previous_choice = ""
        self.count = 0
        self.warning_wait = 60
        self.set_action("idle")

    def update(self, tilemap):
        if self.choice not in ["push_L", "push_R"]:
            for i in range(7):
                if str(23) + ";" + str(-60 - i*1) in self.scene.tilemap.tilemap:
                    del self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)]
            for i in range(7):
                if str(40) + ";" + str(-60 - i*1) in self.scene.tilemap.tilemap:
                    del self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)]

        if self.scene.player.rect().colliderect(self.pos[0] - self.active_radius, self.pos[1] - self.active_radius,
                                                self.active_radius*2, self.active_radius*2) and not self.active:
            self.scene.boss_encounter = True
            self.activate()

        if self.hitbox_active:
            if self.scene.player.rect().colliderect(self.rect()) and not self.scene.player.dashing:
                dis = (self.scene.player.pos[0] - self.pos[0], self.scene.player.pos[1] - self.pos[1])
                if not self.scene.player.invincible_frame:
                    self.scene.player.hurting = True
                    snd = random.choice(["aris_dmg0", "aris_dmg1", "aris_dmg2", "aris_dmg3"])
                    if not self.gameManager.arisChannel.get_busy():
                        self.gameManager.sounds[snd].play()
                    self.scene.player.hp = max(0, self.scene.player.hp - 7)
                    if not self.scene.player.red_hp:
                        self.scene.player.red_hp = 0.6*7
                    self.scene.player.invincible_frame = 30
                if dis[0] < 0:
                    self.scene.player.velocity[0] = -7
                else:
                    self.scene.player.velocity[0] = 7

        self.set_action("idle")

        if self.enrage_attack:
            self.hurting = True
            if self.volley_wait:
                self.volley_wait = max(0, self.volley_wait - 1)
            else:
                self.raging()

        if self.hp <= self.max_hp / 2 and not self.enrage:
            self.gameManager.sounds["yuuka_rage"].play()
            self.enrage = True
            self.enrage_attack = True
            self.invincible = True
            self.inAction = False
            self.count = 0
            self.previous_choice = self.choice
            self.choice = "raging"
            self.dx = 0
            self.velocity[1] = 0
            self.waitTimer = 35
            self.pos[0] = self.topleft[0] + self.room_w / 2 - self.rect().width / 2
            self.pos[1] = self.topleft[1] + self.room_h / 2 - self.rect().height / 2

        if self.active and not self.inAction and not self.enrage_attack:
            if self.waitTimer >= 10:
                self.waitTimer = max(0, self.waitTimer - 1)
            elif self.waitTimer > 0:
                self.waitTimer = max(0, self.waitTimer - 1)
                self.teleport = True
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
                elif self.choice == "push_L":
                    self.push_L()
                elif self.choice == "push_R":
                    self.push_R()

                self.waitTimer = 50
        elif self.inAction and not self.enrage_attack:
            if self.choice == "smash":
                self.smash()
            elif self.choice == "dual_volleyL":
                self.dual_volleyL()
            elif self.choice == "dual_volley_R":
                self.dual_volleyR()
            elif self.choice == "split_bullet":
                self.split_bullet()
            elif self.choice == "push_L":
                self.push_L()
            elif self.choice == "push_R":
                self.push_R()

        super().update(tilemap)

    def hit_rect(self):
        return pygame.Rect(self.rect().centerx - 30, self.rect().bottom - 64, 60, 64)

    def render(self, surf, offset=(0, 0)):
        if not self.teleport:
            super().render(surf, offset)

    def death(self):
        if self.hp <= 0:
            self.gameManager.sounds["yuuka_die"].play()
            self.gameManager.sounds["fell"].play()
            for i in range(7):
                if str(23) + ";" + str(-60 - i*1) in self.scene.tilemap.tilemap:
                    del self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)]
            for i in range(7):
                if str(40) + ";" + str(-60 - i*1) in self.scene.tilemap.tilemap:
                    del self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)]
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

    #MOVES = ["smash", "dual_volleyL", "dual_volley_R", "split_bullet", "push_L", "push_R"]
    def deciding(self):
        if self.previous_choice == "smash":
            self.choice = random.choices(MOVES, weights=[0.05, 0.26, 0.26, 0.21, 0.11, 0.11], k=1)[0]
        elif self.previous_choice == "dual_volleyL":
            self.choice = random.choices(MOVES, weights=[0.12, 0.15, 0.27, 0.22, 0.12, 0.12], k=1)[0]
        elif self.previous_choice == "dual_volley_R":
            self.choice = random.choices(MOVES, weights=[0.12, 0.27, 0.15, 0.22, 0.12, 0.12], k=1)[0]
        elif self.previous_choice == "split_bullet":
            self.choice = random.choices(MOVES, weights=[0.12, 0.27, 0.27, 0.1, 0.12, 0.12], k=1)[0]
        elif self.previous_choice == "push_L":
            self.choice = random.choices(MOVES, weights=[0.12, 0.27, 0.27, 0.22, 0.0, 0.12], k=1)[0]
        elif self.previous_choice == "push_R":
            self.choice = random.choices(MOVES, weights=[0.12, 0.27, 0.27, 0.22, 0.12, 0.0], k=1)[0]
        else:
            self.choice = random.choices(MOVES, weights=[0.1, 0.25, 0.25, 0.2, 0.1, 0.1], k=1)[0]
        self.previous_choice = self.choice

    def raging(self):
        if self.count == 0:
            self.velocity[1] = 10
            self.scene.projectiles.clear()

        if self.collisions['down']:
            self.velocity[1] = 0
            self.count += 1
            self.pos[0] = self.topleft[0] + self.room_w/2 - self.rect().width/2
            self.pos[1] = self.topleft[1] + self.room_h/2 - self.rect().height/2
            self.scene.player.dy = -10
            for i in range(3):
                del self.scene.tilemap.tilemap[str(26 + i * 5) + ";" + str(-59)]
                del self.scene.tilemap.tilemap[str(27 + i * 5) + ";" + str(-59)]
                self.scene.tilemap.tilemap[str(26 + i * 5) + ";" + str(-59)] = {
                    'type': "chamberSpike", 'variant': 9, 'pos': [26 + i*5, -59],
                    'behaviour': "normal"}
                self.scene.tilemap.tilemap[str(27 + i * 5) + ";" + str(-59)] = {
                    'type': "chamberSpike", 'variant': 11, 'pos': [27 + i*5, -59],
                    'behaviour': "normal"}

        if self.count >= 1:
            if self.first_phaseTimer:
                self.first_phaseTimer = max(0, self.first_phaseTimer - 1)
            else:
                self.scene.player.dy = 0
                self.volley_wait = 1

                angle = math.radians(self.angle)
                bullet_x = math.sin(angle) * 3
                bullet_y = math.cos(angle) * 3
                if self.count % 4 == 1:
                    self.gameManager.sounds["gunshot"].play()
                self.scene.projectiles.append(
                    [[self.rect().centerx,
                      self.rect().centery],
                     [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 2])
                self.angle += 10
                self.angle %= 360

                self.count += 1
                if self.count == 73:
                    self.inAction = False
                    self.invincible = False
                    self.count = 0
                    self.enrage_attack = False
                    self.hurting = False

    def gravity(self):
        pass

    def smash(self):
        self.teleport = False
        if self.smash_wait >= 15:
            self.pos[0] = self.scene.player.rect().centerx - self.size[0] / 2
            self.pos[1] = self.scene.player.rect().top - self.size[1] - 20
            self.smash_wait = max(0, self.smash_wait - 1)
        elif self.smash_wait > 0:
            self.smash_wait = max(0, self.smash_wait - 1)
        else:
            self.hitbox_active = True
            self.velocity[1] = 10
            self.smash_wait = max(0, self.smash_wait - 1)

            if self.hit_rect().centery >= self.botleft[1]:
                self.velocity[1] = 0
                self.smash_wait = 45

                self.count += 1
                if self.enrage:
                    if self.count == 5:
                        self.inAction = False
                        self.hitbox_active = False
                        self.count = 0
                else:
                    if self.count == 3:
                        self.inAction = False
                        self.hitbox_active = False
                        self.count = 0

    def dual_volleyL(self):
        self.teleport = False

        if self.count == 0:
            self.pos[0] = self.topleft[0] + 32*2
            self.pos[1] = self.topleft[1] + 32*2
            self.dx = 5
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        if self.volley_wait:
            self.volley_wait = max(0, self.volley_wait - 1)
        else:
            self.gameManager.sounds["gunshot"].play()
            for angle in target_angle:
                bullet_x = math.sin(angle)*7
                bullet_y = math.cos(angle)*7
                self.scene.projectiles.append(
                    [[self.rect().centerx,
                      self.rect().centery],
                     [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 3])
            self.volley_wait = 10

        if self.EuclideanDistance(self.pos, self.topright) < 32*4:
            self.dx = 0
            self.inAction = False
            self.count = 0

    def dual_volleyR(self):
        self.teleport = False

        if self.count == 0:
            self.pos[0] = self.topright[0] - 32*2
            self.pos[1] = self.topright[1] + 32*2
            self.dx = -5
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        if self.volley_wait:
            self.volley_wait = max(0, self.volley_wait - 1)
        else:
            self.gameManager.sounds["gunshot"].play()
            for angle in target_angle:
                bullet_x = math.sin(angle)*7
                bullet_y = math.cos(angle)*7
                self.scene.projectiles.append(
                    [[self.rect().centerx,
                      self.rect().centery],
                     [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 3])
            self.volley_wait = 10

        if self.EuclideanDistance(self.pos, self.topleft) < 32*4:
            self.dx = 0
            self.inAction = False
            self.count = 0

    def split_bullet(self):
        self.teleport = False

        if self.count == 0:
            self.pos[0] = self.topleft[0] + self.room_w/2 - self.rect().width/2
            self.pos[1] = self.topleft[1] + self.room_h/2 - self.rect().height/2
            self.count += 1

        target_angle = QUAD_ANGLES if not self.enrage else OCT_ANGLES

        self.gameManager.sounds["gunshot"].play()
        for angle in target_angle:
            bullet_x = math.sin(angle)*5
            bullet_y = math.cos(angle)*5
            self.scene.special_bullets.append(
                [[self.rect().centerx,
                  self.rect().centery],
                 [bullet_x, bullet_y], 0, self.gameManager.assets['smg_bullet'], 7, "split"])

        self.inAction = False
        self.count = 0

    def push_L(self):
        self.teleport = False

        if self.count == 0:
            self.pos[0] = self.topright[0] - 32*2
            self.pos[1] = self.topright[1] + 32*2
            if abs(self.scene.player.pos[0] - self.topleft[0]) < 32*4:
                self.scene.player.velocity[0] = 7
            self.count += 1
            for i in range(7):
                if i == 0:
                    self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 14, 'pos': [23, -60 - i*1],
                        'behaviour': "normal"}
                elif i == 6:
                    self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 12, 'pos': [23, -60 - i*1],
                        'behaviour': "normal"}
                else:
                    self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 13, 'pos': [23, -60 - i*1],
                        'behaviour': "normal"}
        elif self.count in range(1, 120):
            if not self.count % 2:
                self.scene.player.velocity[0] += -0.8
            self.count += 1
        else:
            for i in range(7):
                del self.scene.tilemap.tilemap[str(23) + ";" + str(-60 - i*1)]
            self.scene.player.velocity[0] = 0
            self.count = 0
            self.inAction = False

    def push_R(self):
        self.teleport = False

        if self.count == 0:
            self.pos[0] = self.topleft[0] + 32*2
            self.pos[1] = self.topleft[1] + 32*2
            if abs(self.topright[0] - self.scene.player.pos[0]) < 32*4:
                self.scene.player.velocity[0] = -7
            self.count += 1
            for i in range(7):
                if i == 0:
                    self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 14, 'pos': [40, -60 - i*1],
                        'behaviour': "normal"}
                elif i == 6:
                    self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 12, 'pos': [40, -60 - i*1],
                        'behaviour': "normal"}
                else:
                    self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)] = {
                        'type': "chamberSpike", 'variant': 13, 'pos': [40, -60 - i*1],
                        'behaviour': "normal"}
        elif self.count in range(1, 120):
            if not self.count % 2:
                self.scene.player.velocity[0] += 0.8
            self.count += 1
        else:
            for i in range(7):
                del self.scene.tilemap.tilemap[str(40) + ";" + str(-60 - i*1)]
            self.scene.player.velocity[0] = 0
            self.count = 0
            self.inAction = False
