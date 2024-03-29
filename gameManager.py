import pygame, pygame.freetype

from script.utils import load_image, load_images, Animation
from mainMenu import MainMenu
from mainGame import MainGame

# icon = pygame.image.load("artwork/sob.png")
# pygame.display.set_icon(icon)


class GameManager:
    def run(self):
        self.currentState.run()

    def changeState(self, newState):
        del self.currentState
        if newState == "main_game":
            self.currentState = MainGame(self)
        elif newState == "main_menu":
            self.currentState = MainMenu(self)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

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
        self.cameraSize = pygame.Rect

        self.assets = {
            "chamber": load_images("tilemap/chamber"),
            "chamberBG": load_images("tilemap/chamberBG"),
            "chamberSpike": load_images("tilemap/chamberSpike"),
            "stairs": load_images("tilemap/stairs"),
            "platform": load_images("tilemap/platform"),
            "background": load_image("tilemap/bg/Layers/1.png"),
            "clouds": load_images("tilemap/clouds"),
            "bushes": load_images("tilemap/objects/Bushes"),
            "grass": load_images("tilemap/objects/Grass"),
            "pointers": load_images("tilemap/objects/Pointers"),
            "ridges": load_images("tilemap/objects/Ridges"),
            "stones": load_images("tilemap/objects/Stones"),
            "trees": load_images("tilemap/objects/Trees"),
            "willows": load_images("tilemap/objects/Willows"),
            "spawners": load_images("tilemap/spawner"),

            "box/idle": Animation(load_images("tilemap/objects/Boxes"), img_dur=1),

            "player/idle": Animation(load_images("sprite/aris/idle"), img_dur=8),
            "player/run": Animation(load_images("sprite/aris/run"), img_dur=4),
            "player/prejump": Animation(load_images("sprite/aris/prejump"), img_dur=5),
            "player/jump": Animation(load_images("sprite/aris/jump"), img_dur=5),
            "player/dash": Animation(load_images("sprite/aris/dash"), img_dur=5),
            "player/land": Animation(load_images("sprite/aris/land"), img_dur=5),
            "player/shooting": Animation(load_images("sprite/aris/shooting"), img_dur=3),
            "player/fall": Animation(load_images("sprite/aris/fall"), img_dur=5),
            "player/wallslide": Animation(load_images("sprite/aris/wallslide"), img_dur=5),
            "player/fallAlt": Animation(load_images("sprite/aris/fallAlt"), img_dur=5),
            "player/landAlt": Animation(load_images("sprite/aris/landAlt"), img_dur=5),
            "player/wallslideAlt": Animation(load_images("sprite/aris/wallslideAlt"), img_dur=5),
            "player/jumpAlt": Animation(load_images("sprite/aris/jumpAlt"), img_dur=5),
            "player/prejumpAlt": Animation(load_images("sprite/aris/prejumpAlt"), img_dur=5),
            "player/idleAlt": Animation(load_images("sprite/aris/idleAlt"), img_dur=8),
            "player/runAlt": Animation(load_images("sprite/aris/runAlt"), img_dur=4),

            "gunner/idle": Animation(load_images("sprite/kei/idle"), img_dur=8),
            "gunner/run": Animation(load_images("sprite/kei/run"), img_dur=4),
            "gunner/prejump": Animation(load_images("sprite/kei/prejump"), img_dur=5),
            "gunner/jump": Animation(load_images("sprite/kei/jump"), img_dur=5),
            "gunner/land": Animation(load_images("sprite/kei/land"), img_dur=5),
            "gunner/fall": Animation(load_images("sprite/kei/fall"), img_dur=5),

            "gun": load_image("sprite/gun/gun.png"),
            "shooting": Animation(load_images("sprite/gun/shooting"), img_dur=2, loop=False),
            "ally_bullet": load_image("sprite/bullet/bullet0.png"),
            "enemy_bullet": load_image("sprite/bullet/bullet2.png"),
            "charged_bullet": load_image("sprite/bullet/bullet1.png"),

            "particle/leaf": Animation(load_images("particles/leaf"), img_dur=20, loop=False),
            "particle/particle": Animation(load_images("particles/particle"), img_dur=6, loop=False),
            "particle/afterimage": Animation(load_images("sprite/aris/dash", 75), img_dur=5, loop=False),
            "particle/dead": Animation(load_images("particles/dead"), img_dur=8, loop=False),

            "healthSmol/idle": Animation(load_images("items/HealthSmol"), img_dur=1),
            "healthBig/idle": Animation(load_images("items/HealthBig"), img_dur=1),

            "refresher/idle": Animation(load_images("refresher/idle"), img_dur=8),
            "refresher/used": Animation(load_images("refresher/used"), img_dur=1),
        }
        self.menuAssets = {
            "bg": load_image("image/titlescreen.png"),
        }
        self.fonts = {
            "title": pygame.freetype.Font("./asset/font/Pixellari.ttf", 40),
            "smol": pygame.freetype.Font("./asset/font/Pixellari.ttf", 15),
            "big": pygame.freetype.Font("./asset/font/Pixellari.ttf", 30),
        }
        self.fontSmol = pygame.freetype.Font("./asset/font/Pixellari.ttf", 20)

        self.currentState = None
        self.changeState("main_menu")
        self.isRunning = True

