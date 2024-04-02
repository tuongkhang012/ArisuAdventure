import pygame
import json
from buttonRect import Button


class EndScene:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.titleButton = Button("TITLE", (self.gameManager.SCREENWIDTH / 2 - 60 - 100, 680), (120, 40), 0, 0,
                                  [255, 210, 159], [100, 0, 35],
                                  self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])
        self.quitButton = Button("QUIT", (self.gameManager.SCREENWIDTH / 2 - 50 + 100, 680), (100, 40), 0, 0,
                                 [255, 210, 159], [100, 0, 35],
                                 self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])

        pygame.mixer.music.load(self.gameManager.musics["ending"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.03)

    def run(self):
        self.screen.blit(self.gameManager.menuAssets["ending"], (0, 0))

        self.titleButton.render(self.screen)
        self.quitButton.render(self.screen)

        if self.titleButton.update():
            self.gameManager.sounds["click"].play()
            self.gameManager.changeState("main_menu")

        if self.quitButton.update():
            self.gameManager.sounds["click"].play()
            self.gameManager.isRunning = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False
