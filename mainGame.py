import pygame
import random
import math
import os

from script.utils import print_text
from script.clouds import Clouds
from script.player import Player
from script.gunner import Gunner
from script.particle import Particle
from script.tilemap import Tilemap
from script.spark import Spark
from script.box import Box
from script.refresher import Refresher
from script.checkpoint import Checkpoint
from script.neru import Neru
from script.yuuka import Yuuka
from script.kei import Kei

from buttonRect import Button


OCT_ANGLES = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]

class MainGame:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.display = self.gameManager.display
        self.paused = False

        self.movement = [False, False]
        self.pressing = [False, False, False, False]  # UP, DOWN, LEFT, RIGHT

        self.clouds = Clouds(self.gameManager.assets["clouds"], count=30)
        self.smogs = Clouds(self.gameManager.assets["smogs"], count=16)

        self.player = Player(self.gameManager, (0, 0), (30, 42), self)

        self.titleButton = Button("TITLE", (1280/2 - 70, 520), (140, 40), 0, 0,
                                  [255, 210, 159], [100, 0, 35],
                                  self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])

        self.continueButton = Button("CONTINUE", (1280/2 - 105, 580), (210, 40), 0, 0,
                                  [255, 210, 159], [100, 0, 35],
                                  self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])

        self.tilemap = Tilemap(self.gameManager)

        self.hpchange_speed = 5
        self.hpbar_length = 100
        self.hp_ratio = self.player.max_hp / self.hpbar_length
        self.boss_hp_length = 600

        self.level = self.gameManager.data["level"]
        self.player.id = self.gameManager.data["id"]
        self.load_level(self.level)


    def load_level(self, map_id):
        pygame.mixer.music.load(self.gameManager.musics[f"lv{map_id}"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.03)

        self.tilemap.load(f"./levels/{map_id}.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('willows', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 124, 156))

        self.player.hp = self.player.max_hp

        self.enemies = []
        self.objects = []
        self.refreshers = []
        self.body = []
        self.victory_timer = 300

        self.player.dx = 0
        self.player.dy = 0
        self.player.velocity = [0, 0]

        self.boss_music = False
        self.victory_music = False

        self.boss_encounter = False
        self.bonfire_timer = 0

        self.checkpoints = []
        self.bosses = []
        self.keis = []
        id = 1
        for checkpoint in self.tilemap.extract([('checkpoint', 0)]):
            self.checkpoints.append(Checkpoint(self.gameManager, checkpoint['pos'], (32, 32), self, id))
            id += 1

        id = 0
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3),
                                             ('spawners', 4), ('spawners', 5), ('spawners', 6)]):
            if spawner['variant'] == 0:
                if self.player.id == 0:
                    self.player.pos = spawner['pos']
                else:
                    for checkpoint in self.checkpoints:
                        if checkpoint.id == self.player.id:
                            checkpoint.set_action("idle")
                            self.player.pos[0] = checkpoint.pos[0]
                            self.player.pos[1] = checkpoint.pos[1]
            elif spawner['variant'] == 1:
                self.enemies.append(Gunner(self.gameManager, spawner['pos'], (30, 42), self))
            elif spawner['variant'] == 2:
                self.objects.append(Box(self.gameManager, spawner['pos'], (27, 26), self))
            elif spawner['variant'] == 3:
                self.refreshers.append(Refresher(self.gameManager, spawner['pos'], (16, 16), self))
            elif spawner['variant'] == 4:
                self.bosses.append(Neru(self.gameManager, spawner['pos'], (30, 42), self))
            elif spawner['variant'] == 5:
                self.bosses.append(Yuuka(self.gameManager, spawner['pos'], (80, 116), self))
            elif spawner['variant'] == 6:
                if (str(self.level) + ";" + str(id)) not in self.gameManager.data["kei"]:
                    self.keis.append(Kei(self.gameManager, self, self.level, id, spawner['pos'], (32, 32)))
                id += 1

        self.projectiles = []
        self.player_projectiles = []
        self.special_bullets = []
        self.particles = []
        self.sparks = []
        self.items = []

        self.scroll = [self.player.rect().centerx - self.display.get_width() / 2,
                       self.player.rect().centery - self.display.get_height() / 2]
        self.dead = 0
        self.transition = -30

        self.screenshake = 0

    def run(self):
        if not self.paused:
            if self.level == 0:
                self.display.blit(pygame.transform.scale(self.gameManager.menuAssets["main_bg0"], self.display.get_size()), (0, 0))
            elif self.level == 1:
                self.display.blit(pygame.transform.scale(self.gameManager.menuAssets["main_bg1"], self.display.get_size()), (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            # TRANSITION
            if not len(self.bosses):
                self.victory_timer = max(0, self.victory_timer - 1)
                if not self.victory_music:
                    pygame.mixer.music.load(self.gameManager.musics["victory"])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.03)
                    self.gameManager.sounds["win"].play()
                    self.victory_music = True
                if not self.victory_timer:
                    self.transition += 1
                    if self.transition > 30:
                        if self.level == 1:
                            self.gameManager.changeState("ending")
                        self.level = min(self.level + 1, len(os.listdir('levels')) - 1)
                        self.player.id = 0
                        self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            # RESOLVE PLAYER DEATH
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.player.reset()
                    self.load_level(self.level)

            # RESOLVE PLAYER CHARGE
            if self.player.charge > 0:
                self.player.charge = min(31, self.player.charge + 1)

            # MOVING THE CAMERA
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # SPAWNING LEAVES
            for rect in self.leaf_spawners:
                # RANDOM CHANCE
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, (rect.y + 40) + random.random() * (rect.height - 40))
                    self.particles.append(
                        Particle(self.gameManager, "leaf", pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            # SPAWNING CLOUDS
            if self.level == 1:
                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            # SPAWNING CHECKPOINTS
            for checkpoint in self.checkpoints.copy():
                checkpoint.update(self.tilemap)
                checkpoint.render(self.display, offset=render_scroll)

            # SPAWNING ENEMIES
            for enemy in self.enemies.copy():
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)

            # SPAWNING BOSSES
            for boss in self.bosses.copy():
                boss.update(self.tilemap)
                boss.render(self.display, offset=render_scroll)

            for body in self.body.copy():
                body.update(self.tilemap)
                body.render(self.display, offset=render_scroll)

            # SPAWNING OBJECTS
            for object in self.objects.copy():
                object.update(self.tilemap)
                object.render(self.display, offset=render_scroll)

            # SPAWNING ITEMS
            for item in self.items.copy():
                item.update(self.tilemap)
                item.render(self.display, offset=render_scroll)

            for kei in self.keis.copy():
                kei.update()
                kei.render(self.display, offset=render_scroll)

            # SPAWNING REFRESHERS
            for refresher in self.refreshers.copy():
                refresher.update(self.tilemap)
                refresher.render(self.display, offset=render_scroll)

            # SPAWNING PARTICLES
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # DRAWING THE PLAYER UNTIL DEATH
            if not self.dead:
                self.player.dx = (self.movement[1] - self.movement[0]) * 3
                self.player.update(self.tilemap)
                self.player.render(self.display, offset=render_scroll)

            # [(x,y), direction, timer, img, dmg] SPAWNING BULLETS
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1][0]
                projectile[0][1] += projectile[1][1]
                projectile[2] += 1
                img = projectile[3]
                flip_flag = False
                img = pygame.transform.rotate(img, -math.degrees(math.atan2(projectile[1][1], projectile[1][0])))
                if projectile[1][0] < 0:
                    flip_flag = True
                self.display.blit(img,
                                  (projectile[0][0] - render_scroll[0],
                                   projectile[0][1] - render_scroll[1]))
                if flip_flag:
                    check_ahead = (projectile[0][0] + projectile[1][0], projectile[0][1] + img.get_height()/2 + projectile[1][1])
                else:
                    check_ahead = (projectile[0][0] + img.get_width() + projectile[1][0], projectile[0][1] + img.get_height()/2 + projectile[1][1])
                if self.tilemap.solid_check(check_ahead):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark((projectile[0][0] + img.get_width()/2, projectile[0][1] + img.get_height()/2),
                                                 random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                                 2 + random.random(), color=(255, 136, 0)))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif not self.player.dashing:
                    if self.player.rect().colliderect((projectile[0][0], projectile[0][1], img.get_width(), img.get_height())):
                        for i in range(4):
                            self.sparks.append(Spark((projectile[0][0] + img.get_width()/2, projectile[0][1] + img.get_height()/2),
                                                     random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                                     2 + random.random(), color=(255, 136, 0)))
                        self.projectiles.remove(projectile)
                        self.player.hurting = True
                        snd = random.choice(["aris_dmg0", "aris_dmg1", "aris_dmg2", "aris_dmg3"])
                        if not self.gameManager.arisChannel.get_busy():
                            self.gameManager.sounds[snd].play()
                        self.player.hp = max(0, self.player.hp - projectile[4])
                        if not self.player.red_hp:
                            self.player.red_hp = 0.6*projectile[4]
                        else:
                            self.player.red_hp = 0

            # FOR SPECIAL BULLETS [(x,y), direction, timer, img, dmg, type]
            for projectile in self.special_bullets.copy():
                projectile[0][0] += projectile[1][0]
                projectile[0][1] += projectile[1][1]
                projectile[2] += 1
                img = projectile[3]
                flip_flag = False
                img = pygame.transform.rotate(img, -math.degrees(math.atan2(projectile[1][1], projectile[1][0])))
                if projectile[1][0] < 0:
                    flip_flag = True
                self.display.blit(img,
                                  (projectile[0][0] - render_scroll[0],
                                   projectile[0][1] - render_scroll[1]))
                if flip_flag:
                    check_ahead = (
                    projectile[0][0] + 2*projectile[1][0], projectile[0][1] + img.get_height() / 2 + 2*projectile[1][1])
                else:
                    check_ahead = (projectile[0][0] + img.get_width() + 2*projectile[1][0],
                                   projectile[0][1] + img.get_height() / 2 + 2*projectile[1][1])
                if self.tilemap.solid_check(check_ahead):
                    self.special_bullets.remove(projectile)
                    if projectile[5] == "split":
                        for angle in OCT_ANGLES:
                            angle_x = math.sin(angle) * 4
                            angle_y = math.cos(angle) * 4
                            self.projectiles.append([[projectile[0][0], projectile[0][1]], [angle_x, angle_y], 0, projectile[3], 4])

                    for i in range(4):
                        self.sparks.append(
                            Spark((projectile[0][0] + img.get_width() / 2, projectile[0][1] + img.get_height() / 2),
                                  random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                  2 + random.random(), color=(255, 136, 0)))
                elif projectile[2] > 360:
                    self.special_bullets.remove(projectile)
                elif not self.player.dashing:
                    if self.player.rect().colliderect(
                            (projectile[0][0], projectile[0][1], img.get_width(), img.get_height())):
                        for i in range(4):
                            self.sparks.append(
                                Spark((projectile[0][0] + img.get_width() / 2, projectile[0][1] + img.get_height() / 2),
                                      random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                      2 + random.random(), color=(255, 136, 0)))
                        self.special_bullets.remove(projectile)
                        self.player.hurting = True
                        snd = random.choice(["aris_dmg0", "aris_dmg1", "aris_dmg2", "aris_dmg3"])
                        if not self.gameManager.arisChannel.get_busy():
                            self.gameManager.sounds[snd].play()
                        self.player.hp = max(0, self.player.hp - projectile[4])
                        if not self.player.red_hp:
                            self.player.red_hp = 0.6 * projectile[4]
                        else:
                            self.player.red_hp = 0

            # SPAWNING PLAYER BULLET
            for projectile in self.player_projectiles.copy():
                projectile[0][0] += projectile[1][0]
                projectile[0][1] += projectile[1][1]
                projectile[2] += 1
                img = projectile[3]
                if projectile[1][0] < 0:
                    img = pygame.transform.flip(img, True, False)
                self.display.blit(img,
                                  (projectile[0][0] - render_scroll[0],
                                   projectile[0][1] - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.player_projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark((projectile[0][0] + img.get_width()/2, projectile[0][1] + img.get_height()/2),
                                                 random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                                 2 + random.random(), color=(255, 136, 0)))
                elif projectile[2] > 360:
                    self.player_projectiles.remove(projectile)
                else:
                    for enemy in self.enemies.copy():
                        if enemy.rect().colliderect((projectile[0][0], projectile[0][1], img.get_width(), img.get_height())):
                            self.gameManager.sounds["hit"].play()
                            for i in range(4):
                                self.sparks.append(Spark((projectile[0][0] + img.get_width()/2, projectile[0][1] + img.get_height()/2),
                                                         random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                                         2 + random.random(), color=(255, 136, 0)))
                            enemy.hp -= projectile[4]
                            enemy.hurting = True
                            self.player_projectiles.remove(projectile)
                            break
                    for boss in self.bosses.copy():
                        if boss.rect().colliderect((projectile[0][0], projectile[0][1], img.get_width(), img.get_height())) and not boss.invincible:
                            self.gameManager.sounds["hit"].play()
                            for i in range(4):
                                self.sparks.append(Spark((projectile[0][0] + img.get_width()/2, projectile[0][1] + img.get_height()/2),
                                                         random.random() - 0.5 + (math.pi if projectile[1][0] > 0 else 0),
                                                         2 + random.random(), color=(255, 136, 0)))
                            boss.hp = max(0, boss.hp - projectile[4])
                            boss.hurting = True
                            self.player_projectiles.remove(projectile)
                            break

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            if self.level == 0:
                self.smogs.update()
                self.smogs.render(self.display, offset=render_scroll)

            if not len(self.bosses) and self.victory_timer > 210:
                self.banner("CORRECTED", (255, 0, 0), self.gameManager.fonts["title"], self.display)

            if self.bonfire_timer:
                self.banner("CHECKPOINT", (255, 102, 0), self.gameManager.fonts["title"], self.display)
                self.bonfire_timer = max(0, self.bonfire_timer - 1)

            self.advanced_hpbar()
            if self.boss_encounter:
                if not self.boss_music:
                    if type(self.bosses[0]) == Neru:
                        pygame.mixer.music.load(self.gameManager.musics["neru"])
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.03)
                        self.gameManager.sounds["neru_start"].play()
                    elif type(self.bosses[0]) == Yuuka:
                        pygame.mixer.music.load(self.gameManager.musics["yuuka"])
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.03)
                        self.gameManager.sounds["yuuka_start"].play()
                    self.boss_music = True
                self.boss_hpbar()

            if not len(self.keis):
                print_text(self.display, "All keis collected", (self.display.get_width() - 126, 5), self.gameManager.fonts["smol"], color = (255, 255, 255))

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255,255,255), (self.display.get_width()//2, self.display.get_height()//2), (30 - abs(self.transition)) * 12)
                transition_surf.set_colorkey((255,255,255))
                self.display.blit(transition_surf, (0,0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake/2, random.random() * self.screenshake - self.screenshake/2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)

            for enemy in self.enemies.copy():
                enemy.death()
            for boss in self.bosses.copy():
                boss.death()
            if not self.dead:
                self.player.death()
        else:
            pygame.draw.rect(self.screen, (255, 210, 159), (80, 60, 1120, 600))
            pygame.draw.rect(self.screen, (229, 148, 57), (80, 60, 1120, 600), 3)

            print_text(self.screen, "PAUSED", (1280/2 - 70, 100), self.gameManager.fonts['title'], color=(229, 64, 64))
            if len(self.keis):
                self.screen.blit(pygame.transform.scale(self.gameManager.assets["keiBlack"], (128,128)), (1280/2 - 64, 720/2 - 64 - 40))
                print_text(self.screen, "Still " + str(len(self.keis)) + " Keis remains!", (1280 / 2 - 170, 720/2 + 50), self.gameManager.fonts['title'],
                           color=(0, 0, 0))
            else:
                self.screen.blit(pygame.transform.scale(self.gameManager.assets["kei"], (128,128)), (1280/2 - 64, 720/2 - 64 - 40))
                print_text(self.screen, "All Keis has been collected!", (1280 / 2 - 230, 720 / 2 + 50),
                           self.gameManager.fonts['title'],
                           color=(0, 0, 0))

            self.titleButton.render(self.screen)
            self.continueButton.render(self.screen)

            if self.titleButton.update():
                self.gameManager.changeState("main_menu")
            if self.continueButton.update():
                self.paused = not self.paused

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.data["level"] = self.level
                self.gameManager.data["id"] = self.player.id
                self.gameManager.isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not self.paused:
                    self.movement[0] = True
                    self.pressing[2] = True
                if event.key == pygame.K_RIGHT and not self.paused:
                    self.movement[1] = True
                    self.pressing[3] = True
                if event.key == pygame.K_UP and not self.paused:
                    self.pressing[0] = True
                if event.key == pygame.K_DOWN and not self.paused:
                    self.pressing[1] = True
                    self.player.duck = True
                if event.key == self.gameManager.keys["fire"] and not self.paused:
                    self.player.charge = 1
                if event.key == self.gameManager.keys["jump"] and not self.paused:
                    self.player.jump()
                if event.key == self.gameManager.keys["dash"] and not self.paused:
                    self.player.dash(self.pressing)
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    self.pressing = [False, False, False, False]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and not self.paused:
                    self.movement[0] = False
                    self.pressing[2] = False
                if event.key == pygame.K_RIGHT and not self.paused:
                    self.movement[1] = False
                    self.pressing[3] = False
                if event.key == pygame.K_UP and not self.paused:
                    self.pressing[0] = False
                if event.key == pygame.K_DOWN and not self.paused:
                    self.pressing[1] = False
                    self.player.duck = False
                if event.key == self.gameManager.keys["fire"] and not self.paused:
                    self.player.shoot()

    def advanced_hpbar(self):
        self.player.hp = min(self.player.hp + self.player.red_hp / 360, self.player.hp + self.player.red_hp)
        self.player.red_hp = max(0.0, self.player.red_hp - self.player.red_hp / 360)

        hpbar_width = int(self.player.hp / self.hp_ratio)
        red_hpbar_width = int(self.player.red_hp / self.hp_ratio)
        hpbar = pygame.Rect(10, 10, hpbar_width, 10)
        red_hpbar = pygame.Rect(hpbar.right, 10, red_hpbar_width, 10)

        pygame.draw.rect(self.display, (50, 50, 50), (10, 10, self.hpbar_length, 10)) # THE BACKGROUND
        pygame.draw.rect(self.display, (76, 231, 231), hpbar) # THE CURRENT HP
        pygame.draw.rect(self.display, (255, 0, 0), red_hpbar)
        pygame.draw.rect(self.display, (0, 0, 0), (10, 10, self.hpbar_length, 10), 1) # THE BORDER

    def boss_hpbar(self):
        text_surf, text_rect = self.gameManager.fonts['boss'].render(self.bosses[0].name, (255, 255, 255))
        hpbar_width = int(self.bosses[0].hp / self.bosses[0].max_hp * self.boss_hp_length)
        hpbar = pygame.Rect(20, 330, hpbar_width, 10)

        self.display.blit(text_surf, (20, 310))
        pygame.draw.rect(self.display, (50, 50, 50), (20, 330, self.boss_hp_length, 10)) # THE BACKGROUND
        pygame.draw.rect(self.display, (255, 41, 41), hpbar) # THE CURRENT HP
        pygame.draw.rect(self.display, (0, 0, 0), (20, 330, self.boss_hp_length, 10), 1) # THE BORDER

    def entities_around(self, rect):
        entities = []
        for object in self.objects:
            if object.rect().colliderect(rect):
                entities.append(object)
        return entities

    def banner(self, text, color, font, display):
        text_surf, text_rect = font.render(text, color)
        s = pygame.Surface((display.get_width(), 60))
        s.set_alpha(190)
        s.fill((0, 0, 0))
        display.blit(s, (0, display.get_height()/2 - 30))
        display.blit(text_surf, (display.get_width()/2 - text_rect.w/2, display.get_height()/2 - text_rect.h/2))

