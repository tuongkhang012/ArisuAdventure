import pygame

from script.utils import load_image, load_images, Animation
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
            "background": load_image("tilemap/bg/Layers/1.png"),
            "clouds": load_images("tilemap/clouds"),
            "bushes": load_images("tilemap/objects/Bushes"),
            "grass": load_images("tilemap/objects/Grass"),
            "pointers": load_images("tilemap/objects/Pointers"),
            "ridges": load_images("tilemap/objects/Ridges"),
            "stones": load_images("tilemap/objects/Stones"),
            "trees": load_images("tilemap/objects/Trees"),
            "willows": load_images("tilemap/objects/Willows"),

            "player/idle": Animation(load_images("sprite/aris/idle"), img_dur=8),
            "player/run": Animation(load_images("sprite/aris/run"), img_dur=4),
            "player/prejump": Animation(load_images("sprite/aris/prejump"), img_dur=5),
            "player/jump": Animation(load_images("sprite/aris/jump"), img_dur=5),
            "player/dash": Animation(load_images("sprite/aris/dash"), img_dur=5),
            "player/land": Animation(load_images("sprite/aris/land"), img_dur=5),
            "player/shooting": Animation(load_images("sprite/aris/shooting"), img_dur=3),
            "player/fall": Animation(load_images("sprite/aris/fall"), img_dur=5),
        }

        self.states = {"main_menu": MainMenu(self), "main_game": MainGame(self)}
        self.changeState("main_menu")
        self.isRunning = True

