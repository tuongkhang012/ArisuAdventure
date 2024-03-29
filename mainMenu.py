import pygame
from buttonRect import Button

class MainMenu:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock
        self.playButton = Button("NEW GAME", (self.gameManager.SCREENWIDTH / 2 - 103, 460), (206, 40), 0, 0,
                                 [255, 210, 159], [100, 0, 35],
                                 self.gameManager.fonts['title'], [229,64,64], [184, 0, 64], [229,148,57])
        self.continueButton = Button("CONTINUE", (self.gameManager.SCREENWIDTH / 2 - 105, 520), (210, 40), 0, 0,
                                     [255, 210, 159], [100, 0, 35],
                                     self.gameManager.fonts['title'], [229,64,64], [184, 0, 64], [229,148,57])
        self.greyContinueButton = Button("CONTINUE", (self.gameManager.SCREENWIDTH / 2 - 105, 520), (210, 40), 0, 0,
                                         [200, 200, 200], [100, 0, 35],
                                         self.gameManager.fonts['title'], border=[0, 0, 0])

    def run(self):
        self.screen.blit(self.gameManager.menuAssets["bg"], (0, 0))

        self.playButton.render(self.screen)
        self.continueButton.render(self.screen)

        if self.playButton.update():
            self.gameManager.changeState("main_game")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False