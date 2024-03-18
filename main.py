import pygame
import sys
import json
import random

# variable
pygame.font.init()
SCREENWIDTH, SCREENHEIGHT = 854, 480
FPS = 30
CAPTION = "Leave Sensei alone!"
# icon = pygame.image.load("artwork/sob.png")
# pygame.display.set_icon(icon)
PIXEL_FONT_BIG = pygame.font.Font("font/PixelGameFont.ttf", 80)
PIXEL_FONT = pygame.font.Font("font/PixelGameFont.ttf", 40)
PIXEL_FONT_SMALL = pygame.font.Font("font/PixelGameFont.ttf", 15)

# save game
# try:
#     with open('save/data.json') as score_file:
#         data = json.load(score_file)
#     print('save file found!')
# except FileNotFoundError:
#     print('no save file found! Creating a new save file')
#     data = {
#         "hiscore": 0,
#     }


def drawText(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(CAPTION)
        self.gameStateManager = None

        self.states = {"main_menu": None}

    def run(self):
        while 1:
            # self.states[self.gameStateManager.getState()].run()
            #
            # pygame.display.flip()
            # self.clock.tick(FPS)

class GameStateManager:
    def __init__(self, currentState, bgm):
        self.currentState = currentState
        # bgm
        self.bgm = bgm
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.play(-1)  # -1 = unlimited loop
        pygame.mixer.music.set_volume(0.05)

    def getState(self):
        return self.currentState

    def setState(self, state, bgm, volume=0.05, c=False):
        self.currentState = state
        self.bgm = bgm
        if not c:
            pygame.mixer.music.load(self.bgm)
            pygame.mixer.music.play(-1)  # -1 = unlimited loop
            pygame.mixer.music.set_volume(volume)
        else:
            pygame.mixer.music.set_volume(volume)


if __name__ == '__main__':
    game = Game()
    game.run()
