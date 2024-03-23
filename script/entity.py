import pygame

class PhysicsEntity:
    def __init__(self, gameManager, e_type, pos, size):
        self.gameManager = gameManager
        self.type = e_type
        self.pos = list(pos) # TOP LEFT IS THE ORIGIN
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action = ""
        self.anim_offset = (0, -8)
        self.flip = False
        self.set_action("idle")

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]

        #pygame.draw.rect(self.gameManager.display, (255, 0, 0), pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, True):
            if entity_rect.colliderect(rect):
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

        self.pos[1] += frame_movement[1]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos, True):
            if entity_rect.colliderect(rect):
                #pygame.draw.rect(self.gameManager.display, (0, 255, 0), rect)
                if frame_movement[1] > 0: # MOVING DOWN
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0: # MOVING UP
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.3)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        #TAKE EACH FRAME FROM THE ANIMATION AND BLIT IT
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                  (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        #surf.blit(self.gameManager.assets["player"], (self.pos[0] - offset[0], self.pos[1] - 8 - offset[1]))

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.gameManager.assets[self.type + "/" + self.action].copy()

class Player(PhysicsEntity):
    def __init__(self, gameManager, pos, size):
        super().__init__(gameManager, "player", pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.air_time += 1
        if self.collisions['down']:
            if self.air_time > 4:
                self.set_action("land")
            self.air_time = 0

        if self.velocity[1] < 0:
            self.set_action("jump")

        if self.velocity[1] > 0 and self.air_time > 4:
            self.set_action("fall")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")