import pygame

from script.utils import load_image, load_images
from mainMenu import MainMenu
from mainGame import MainGame

# icon = pygame.image.load("artwork/sob.png")
# pygame.display.set_icon(icon)


class GameManager:
    def run(self):
        self.currentState.run()

    def changeState(self, newState):
        self.currentState = self.states[newState]
        self.currentState.gameManager = self

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.SCREENWIDTH = 1280
        self.SCREENHEIGHT = 720
        self.FPS = 30
        self.CAPTION = "Arisu Adventure"
        self.icon = None

        pygame.display.set_caption(self.CAPTION)
        # icon = pygame.image.load("artwork/sob.png")
        # pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        # FOR SCALING PURPOSES
        self.display = pygame.Surface((self.SCREENWIDTH / 2,
                                       self.SCREENHEIGHT / 2))
        self.clock = pygame.time.Clock()

        self.assets = {
            "overworld": load_images("tilemap/tiles"),
            "player": load_image("sprite/arisu.png"),
            "background": load_image("tilemap/bg/Layers/1.png"),
            "clouds": load_images("tilemap/clouds"),
        }

        self.states = {"main_menu": MainMenu(self), "main_game": MainGame(self)}
        self.changeState("main_menu")
        self.isRunning = True

