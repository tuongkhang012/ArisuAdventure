import pygame

class PhysicsEntity:
    def __init__(self, gameManager, e_type, pos, size):
        self.gameManager = gameManager
        self.type = e_type
        self.pos = list(pos) # TOP LEFT IS THE ORIGIN
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

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

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.gameManager.assets["player"], (self.pos[0] - offset[0], self.pos[1] - 8 - offset[1]))