import pygame
import math
import random

from script.particle import Particle

TALL = ["player", "gunner"]
SHORT = ["box"]
HARD_OBJECTS = ["box"]

class PhysicsEntity:
    def __init__(self, gameManager, scene, e_type, pos, size):
        self.gameManager = gameManager
        self.scene = scene
        self.type = e_type
        self.pos = list(pos) # TOP LEFT IS THE ORIGIN
        self.size = size
        self.dx = 0
        self.dy = 0
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.entity_col = {'up': [], 'down': [], 'left': [], 'right': []}

        self.action = ""
        self.anim_offset = (0, -8)
        self.flip = False
        self.hurting = False
        self.set_action("idle")

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.entity_col = {'up': [], 'down': [], 'left': [], 'right': []}
        frame_movement = (self.dx + self.velocity[0], self.dy + self.velocity[1])
        up_rect = pygame.Rect(self.pos[0] + self.size[0]/2, self.pos[1] - 2, 8, 2)
        down_rect = pygame.Rect(self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1], 8, 2)
        left_rect = pygame.Rect(self.pos[0] - 2, self.pos[1] + self.size[1]/2, 2, 8)
        right_rect = pygame.Rect(self.pos[0] + self.size[0], self.pos[1] + self.size[1]/2, 2, 8)

        self.entity_col['up'] = self.scene.entities_around(up_rect)
        self.entity_col['down'] = self.scene.entities_around(down_rect)
        self.entity_col['left'] = self.scene.entities_around(left_rect)
        self.entity_col['right'] = self.scene.entities_around(right_rect)

        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, True if self.type in TALL else False):
            rect, behaviour = rect
            if entity_rect.colliderect(rect):
                if behaviour == "normal":
                    #pygame.draw.rect(self.gameManager.display, (0, 0, 255), rect)
                    if frame_movement[0] > 0: # MOVING RIGHT
                        # MOVE ENTITY BACK TO THE LEFT OF THE TILE
                        entity_rect.right = rect.left
                        self.collisions['right'] = True
                    if frame_movement[0] < 0: # MOVING LEFT
                        # MOVE ENTITY BACK TO THE RIGHT OF THE TILE
                        entity_rect.left = rect.right
                        self.collisions['left'] = True
                    # UPDATE ENTITY POSITION
                    self.pos[0] = entity_rect.x

        entity_rect = self.rect()
        for entity in self.entity_col['left']:
            if entity.type in HARD_OBJECTS:
                if frame_movement[0] < 0:
                    entity_rect.left = entity.rect().right
                    self.pos[0] = entity_rect.x
                    self.collisions['left'] = True

        entity_rect = self.rect()
        for entity in self.entity_col['right']:
            if entity.type in HARD_OBJECTS:
                if frame_movement[0] > 0:
                    entity_rect.right = entity.rect().left
                    self.pos[0] = entity_rect.x
                    self.collisions['right'] = True

        self.pos[1] += frame_movement[1]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, True if self.type in TALL else False):
            rect, behaviour = rect
            if entity_rect.colliderect(rect):
                if behaviour == "normal":
                    #pygame.draw.rect(self.gameManager.display, (0, 255, 0), rect)
                    if frame_movement[1] > 0: # MOVING DOWN
                        entity_rect.bottom = rect.top
                        self.collisions['down'] = True
                    if frame_movement[1] < 0: # MOVING UP
                        entity_rect.top = rect.bottom
                        self.collisions['up'] = True
                    self.pos[1] = entity_rect.y

        entity_rect = self.rect()
        for entity in self.entity_col['up']:
            if entity.type in HARD_OBJECTS:
                if frame_movement[1] < 0:
                    entity_rect.top = entity.rect().bottom
                    self.pos[1] = entity_rect.y
                    self.collisions['up'] = True

        entity_rect = self.rect()
        for entity in self.entity_col['down']:
            if entity.type in HARD_OBJECTS:
                if frame_movement[1] > 0:
                    entity_rect.bottom = entity.rect().top
                    self.pos[1] = entity_rect.y
                    self.collisions['down'] = True

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, True if self.type in TALL else False):
            rect, behaviour = rect
            if entity_rect.colliderect(rect):
                if behaviour in ["ramps_r", "ramps_l"]:
                    #GET PLAYER POS RELATIVE TO RAMP
                    rel_x = entity_rect.x - rect.x

                    if behaviour == "ramps_l":
                        #GET Y VALUE OF RAMP AT RELATIVE X
                        pos_height = rel_x + entity_rect.width
                    else:
                        pos_height = tilemap.tile_size - rel_x

                    pos_height = min(pos_height, tilemap.tile_size)
                    pos_height = max(pos_height, 0)

                    target_y = rect.y + tilemap.tile_size - pos_height

                    if entity_rect.bottom > target_y:
                        entity_rect.bottom = target_y
                        self.pos[1] = entity_rect.y

                        self.collisions['down'] = True

        if self.dx > 0:
            self.flip = False
        if self.dx < 0:
            self.flip = True

        self.last_movement = [self.dx, self.dy]

        self.gravity()

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        if self.hurting:
            img = self.animation.img().copy()
            rect = img.get_rect()
            wsurface = pygame.Surface(rect.size, pygame.SRCALPHA)
            wsurface.fill((255, 0, 0, 75))
            img.blit(wsurface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.hurting = False
        else:
            img = self.animation.img()
        #TAKE EACH FRAME FROM THE ANIMATION AND BLIT IT
        surf.blit(pygame.transform.flip(img, self.flip, False),
                  (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.gameManager.assets[self.type + "/" + self.action].copy()

    def gravity(self):
        self.velocity[1] = min(5, self.velocity[1] + 0.3)
