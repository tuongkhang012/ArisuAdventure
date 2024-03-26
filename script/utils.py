import pygame, os

BASE_IMG_PATH = 'asset/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def print_text(surface, text, pos, font, alpha=255, color=(0, 0, 0)):
    temp_surf, rect = font.render(text, color)
    temp_surf.set_alpha(alpha)
    surface.blit(temp_surf, list(pos))

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    # TO GET THE CURRENT FRAME
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
