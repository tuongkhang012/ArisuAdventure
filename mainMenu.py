import pygame

class MainMenu:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock

    def run(self):
        self.screen.fill((255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gameManager.changeState("main_game")