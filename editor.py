import pygame, sys, pygame.freetype

from script.utils import load_images, Animation, print_text
from script.tilemap import Tilemap

RENDER_SCALE = 2.0


class Editor:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        self.SCREENWIDTH = 1280
        self.SCREENHEIGHT = 720
        self.FPS = 30
        self.CAPTION = "LEVEL EDITOR"
        self.icon = None

        pygame.display.set_caption(self.CAPTION)

        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        # FOR SCALING PURPOSES
        self.display = pygame.Surface((self.SCREENWIDTH / 2,
                                       self.SCREENHEIGHT / 2))
        self.clock = pygame.time.Clock()

        self.assets = {
            "chamber": load_images("tilemap/chamber"),
            "chamberBG": load_images("tilemap/chamberBG"),
            "chamberSpike": load_images("tilemap/chamberSpike"),

            "stairs": load_images("tilemap/stairs"),
            "platform": load_images("tilemap/platform"),

            "clouds": load_images("tilemap/clouds"),
            "bushes": load_images("tilemap/objects/Bushes"),
            "grass": load_images("tilemap/objects/Grass"),
            "pointers": load_images("tilemap/objects/Pointers"),
            "ridges": load_images("tilemap/objects/Ridges"),
            "stones": load_images("tilemap/objects/Stones"),
            "trees": load_images("tilemap/objects/Trees"),
            "willows": load_images("tilemap/objects/Willows"),
            'spawners': load_images('tilemap/spawner'),
            "onedoorleft": load_images("tilemap/onedoorleft"),
            "signs": load_images("signs"),

            "checkpoint": load_images("checkpoint/untouched"),
        }

        self.movement = [False, False, False, False]
        self.fontSmol = pygame.freetype.Font("./asset/font/Pixellari.ttf", 15)
        self.tilemap = Tilemap(self, tile_size=32)

        try:
            self.tilemap.load("./levels/0.json")
        except FileNotFoundError:
            pass

        self.scroll = [16 - self.display.get_width() / 2, 32 - self.display.get_height() / 2]

        self.tile_list = list(self.assets)
        self.tile_behaviours = ["normal", "platform", "ramps_l", "ramps_r"]
        self.tile_group = 0
        self.tile_variant = 0
        self.tile_behaviour = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.ctrl = False

    def run(self):
        while True:
            self.display.fill((200, 200, 200))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 5
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 5
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            print_text(self.display, "SPAWNPOINT", (5 - render_scroll[0], -15 - render_scroll[1]), self.fontSmol, 200)
            pygame.draw.rect(self.display, (0, 0, 255), (0 - render_scroll[0], 0 - render_scroll[1], 32, 64), 2)

            print_text(self.display, "DEATH LINE", (0 - render_scroll[0], 32*30 - 20 - render_scroll[1]), self.fontSmol, 200)
            pygame.draw.line(self.display, (255, 0, 0), (-500 - render_scroll[0], 32*30 - render_scroll[1]),
                             (500 - render_scroll[0], 32*30 - render_scroll[1]), 1)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            print_text(self.display, "Group: " + self.tile_list[self.tile_group], (40, 5), self.fontSmol, 200)
            print_text(self.display, "Var: " + str(self.tile_variant), (240, 5), self.fontSmol, 200)
            print_text(self.display, "Mode: " + self.tile_behaviours[self.tile_behaviour], (320, 5), self.fontSmol, 200)
            print_text(self.display, "GRID" if self.ongrid else "OFFGRID", (440, 5), self.fontSmol, 200)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos,
                    'behaviour': self.tile_behaviours[self.tile_behaviour]}
            if self.right_clicking:
                if self.ongrid:
                    tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                    if tile_loc in self.tilemap.tilemap:
                        del self.tilemap.tilemap[tile_loc]
                else:
                    for tile in self.tilemap.offgrid_tiles.copy():
                        tile_img = self.assets[tile['type']][tile['variant']]
                        tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                             tile_img.get_width(), tile_img.get_height())
                        if tile_r.collidepoint(mpos):
                            self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(
                                {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant,
                                 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1]),
                                 'behaviour': self.tile_behaviours[self.tile_behaviour]})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    elif self.ctrl:
                        if event.button == 4:
                            self.tile_behaviour = (self.tile_behaviour - 1) % len(self.tile_behaviours)
                        if event.button == 5:
                            self.tile_behaviour = (self.tile_behaviour + 1) % len(self.tile_behaviours)
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save("./levels/0.json")
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)


Editor().run()
