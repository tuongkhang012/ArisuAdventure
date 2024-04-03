import pygame, pygame.freetype

from script.utils import load_image, load_images, Animation
from mainMenu import MainMenu
from mainGame import MainGame
from endScene import EndScene
from option import Option
from intro import Intro


class GameManager:
    def run(self):
        self.currentState.run()

    def changeState(self, newState):
        del self.currentState
        if newState == "main_game":
            self.currentState = MainGame(self)
        elif newState == "main_menu":
            self.currentState = MainMenu(self)
        elif newState == "ending":
            self.currentState = EndScene(self)
        elif newState == "options":
            self.currentState = Option(self)
        elif newState == "intro":
            self.currentState = Intro(self)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        self.SCREENWIDTH = 1280
        self.SCREENHEIGHT = 720
        self.FPS = 30
        self.CAPTION = "Arisu Adventure"
        self.data = {
            "level": 0,
            "id": 0,
            "kei": [],
        }

        pygame.display.set_caption(self.CAPTION)

        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        # FOR SCALING PURPOSES
        self.display = pygame.Surface((self.SCREENWIDTH / 2,
                                       self.SCREENHEIGHT / 2), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.cameraSize = pygame.Rect

        self.arisChannel = pygame.mixer.Channel(7)
        self.icon = load_image("icon/sob.png")
        pygame.display.set_icon(self.icon)

        self.keys = {
            "fire": pygame.K_c,
            "jump": pygame.K_x,
            "dash": pygame.K_z,
        }
        self.assets = {
            "chamber": load_images("tilemap/chamber"),
            "chamberBG": load_images("tilemap/chamberBG"),
            "chamberSpike": load_images("tilemap/chamberSpike"),
            "stairs": load_images("tilemap/stairs"),
            "platform": load_images("tilemap/platform"),
            "clouds": load_images("tilemap/clouds"),
            "smogs": load_images("tilemap/smogs", 170),
            "bushes": load_images("tilemap/objects/Bushes"),
            "grass": load_images("tilemap/objects/Grass"),
            "pointers": load_images("tilemap/objects/Pointers"),
            "ridges": load_images("tilemap/objects/Ridges"),
            "stones": load_images("tilemap/objects/Stones"),
            "trees": load_images("tilemap/objects/Trees"),
            "willows": load_images("tilemap/objects/Willows"),
            "spawners": load_images("tilemap/spawner"),
            "onedoorleft": load_images("tilemap/onedoorleft"),
            "signs": load_images("signs"),

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
            "player/duck": Animation(load_images("sprite/aris/down"), img_dur=5),

            "neru_ded/idle": Animation(load_images("sprite/neru_ded/idle"), img_dur=5),

            "kei": load_image("items/kei/kei.png"),
            "keiBlack": load_image("items/kei/keiBlack.png"),

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
            "smg_bullet": load_image("sprite/bullet/bullet3.png"),
            "charged_bullet": load_image("sprite/bullet/bullet1.png"),

            "particle/leaf": Animation(load_images("particles/leaf"), img_dur=20, loop=False),
            "particle/particle": Animation(load_images("particles/particle"), img_dur=6, loop=False),
            "particle/afterimage": Animation(load_images("sprite/aris/dash", 75), img_dur=5, loop=False),
            "particle/dead": Animation(load_images("particles/dead"), img_dur=8, loop=False),

            "healthSmol/idle": Animation(load_images("items/HealthSmol"), img_dur=1),
            "healthBig/idle": Animation(load_images("items/HealthBig"), img_dur=1),

            "refresher/idle": Animation(load_images("refresher/idle"), img_dur=8),
            "refresher/used": Animation(load_images("refresher/used"), img_dur=1),

            "checkpoint": load_images("checkpoint/untouched"),

            "checkpoint/untouched": Animation(load_images("checkpoint/untouched"), img_dur=1),
            "checkpoint/burn": Animation(load_images("checkpoint/burn"), img_dur=5, loop=False),
            "checkpoint/idle": Animation(load_images("checkpoint/idle"), img_dur=5),

            "neru/idle": Animation(load_images("sprite/neru/idle"), img_dur=8),
            "neru/run": Animation(load_images("sprite/neru/run"), img_dur=4),
            "neru/prejump": Animation(load_images("sprite/neru/prejump"), img_dur=5),
            "neru/jump": Animation(load_images("sprite/neru/jump"), img_dur=5),
            "neru/land": Animation(load_images("sprite/neru/land"), img_dur=5),
            "neru/fall": Animation(load_images("sprite/neru/fall"), img_dur=5),
            "neru/wallslide": Animation(load_images("sprite/neru/wallslide"), img_dur=5),

            "yuuka/idle": Animation(load_images("sprite/yuuka"), img_dur=8),
        }
        self.menuAssets = {
            "menu_bg": load_image("image/titlescreen.png"),
            "main_bg0": load_image("image/main_bg0.png"),
            "main_bg1": load_image("image/main_bg1.jpg"),
            "ending": load_image("image/ending.png"),
            "option": load_image("image/option.png"),
            "intro": load_image("image/intro.jpg"),
        }
        self.fonts = {
            "title": pygame.freetype.Font("./asset/font/Pixellari.ttf", 40),
            "smol": pygame.freetype.Font("./asset/font/Pixellari.ttf", 15),
            "big": pygame.freetype.Font("./asset/font/Pixellari.ttf", 30),
            "border": pygame.freetype.Font("./asset/font/Pixellari.ttf", 42),
            "boss": pygame.freetype.Font("./asset/font/AncientModernTales-a7Po.ttf", 20),
        }
        self.sounds = {
            "click": pygame.mixer.Sound("./asset/sounds/click.mp3"),
            "hit": pygame.mixer.Sound("./asset/sounds/hurt.mp3"),
            "shoot": pygame.mixer.Sound("./asset/sounds/shot.mp3"),
            "gunshot": pygame.mixer.Sound("./asset/sounds/gunshot.mp3"),
            "aris_dmg0": pygame.mixer.Sound("./asset/sounds/aris_dmg0.mp3"),
            "aris_dmg1": pygame.mixer.Sound("./asset/sounds/aris_dmg1.mp3"),
            "aris_dmg2": pygame.mixer.Sound("./asset/sounds/aris_dmg2.mp3"),
            "aris_dmg3": pygame.mixer.Sound("./asset/sounds/aris_dmg3.mp3"),
            "aris_die": pygame.mixer.Sound("./asset/sounds/aris_die.mp3"),
            "dash": pygame.mixer.Sound("./asset/sounds/dash.wav"),
            "checkpoint": pygame.mixer.Sound("./asset/sounds/checkpoint.wav"),
            "fell": pygame.mixer.Sound("./asset/sounds/fell.wav"),
            "neru_rage": pygame.mixer.Sound("./asset/sounds/neru_rage.mp3"),
            "neru_start": pygame.mixer.Sound("./asset/sounds/neru_start.mp3"),
            "neru_die": pygame.mixer.Sound("./asset/sounds/neru_die.mp3"),
            "yuuka_rage": pygame.mixer.Sound("./asset/sounds/yuuka_rage.mp3"),
            "yuuka_start": pygame.mixer.Sound("./asset/sounds/yuuka_start.mp3"),
            "yuuka_die": pygame.mixer.Sound("./asset/sounds/yuuka_die.mp3"),
            "jump": pygame.mixer.Sound("./asset/sounds/jump.mp3"),
            "win": pygame.mixer.Sound("./asset/sounds/panpakapan.wav"),
            "charged_shot": pygame.mixer.Sound("./asset/sounds/charged_shot.wav"),

            "kuyashii": pygame.mixer.Sound("./asset/sounds/kuyashii.mp3"),
            "knock": pygame.mixer.Sound("./asset/sounds/knock.mp3"),
            "retro_success": pygame.mixer.Sound("./asset/sounds/retro_success.mp3"),
            "sad": pygame.mixer.Sound("./asset/sounds/sad.mp3"),
            "angry": pygame.mixer.Sound("./asset/sounds/angry.mp3"),
        }

        self.sounds["hit"].set_volume(0.1)
        self.sounds["shoot"].set_volume(0.1)
        self.sounds["gunshot"].set_volume(0.05)
        self.sounds["aris_dmg0"].set_volume(0.1)
        self.sounds["aris_dmg1"].set_volume(0.1)
        self.sounds["aris_dmg2"].set_volume(0.1)
        self.sounds["aris_dmg3"].set_volume(0.1)
        self.sounds["aris_die"].set_volume(0.1)
        self.sounds["dash"].set_volume(0.1)
        self.sounds["checkpoint"].set_volume(0.1)
        self.sounds["fell"].set_volume(0.05)
        self.sounds["neru_rage"].set_volume(0.1)
        self.sounds["neru_start"].set_volume(0.1)
        self.sounds["neru_die"].set_volume(0.1)
        self.sounds["yuuka_rage"].set_volume(0.1)
        self.sounds["yuuka_start"].set_volume(0.1)
        self.sounds["yuuka_die"].set_volume(0.1)
        self.sounds["jump"].set_volume(0.05)
        self.sounds["win"].set_volume(0.1)
        self.sounds["charged_shot"].set_volume(0.05)
        self.sounds["kuyashii"].set_volume(0.1)
        self.sounds["knock"].set_volume(0.4)
        self.sounds["retro_success"].set_volume(0.1)
        self.sounds["sad"].set_volume(0.1)
        self.sounds["angry"].set_volume(0.2)


        self.musics = {
            "menu": "./asset/music/Encroached Sky.wav",
            "option": "./asset/music/Lemonade Diary.wav",
            "lv0": "./asset/music/Tech N Tech (Hard).wav",
            "lv1": "./asset/music/Ark in the Blood Sky.wav",
            "victory": "./asset/music/Party Time.wav",
            "neru": "./asset/music/Burning Love.wav",
            "yuuka": "./asset/music/kitsunebi.wav",
            "ending": "./asset/music/Ending.ogg",
            "intro": "./asset/music/Pixel Time.wav",
        }
        self.fontSmol = pygame.freetype.Font("./asset/font/Pixellari.ttf", 20)

        self.currentState = None
        self.changeState("main_menu")
        self.isRunning = True

