import pygame
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

        self.SCREENWIDTH = 640
        self.SCREENHEIGHT = 480
        self.FPS = 30
        self.CAPTION = "Arisu Adventure"
        self.icon = None

        pygame.display.set_caption(self.CAPTION)
        # icon = pygame.image.load("artwork/sob.png")
        # pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.states = {"main_menu": MainMenu(self), "main_game": MainGame(self)}
        self.changeState("main_menu")
        self.isRunning = True

