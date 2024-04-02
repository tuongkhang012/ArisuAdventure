import pygame
import json
import os
from buttonRect import Button
from script.utils import print_text


class Option:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock

        pygame.mixer.music.load(self.gameManager.musics["option"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.03)

        self.deleteButton = Button("DELETE SAVE", (self.gameManager.SCREENWIDTH / 2 - 138, 480), (276, 40), 0, 0,
                                 [255, 210, 159], [100, 0, 35],
                                 self.gameManager.fonts['title'], [229,64,64], [184, 0, 64], [229,148,57])
        self.backButton = Button("BACK", (self.gameManager.SCREENWIDTH / 2 - 60, 540), (120, 40), 0, 0,
                                 [255, 210, 159], [100, 0, 35],
                                 self.gameManager.fonts['title'], [229,64,64], [184, 0, 64], [229,148,57])
        self.changeFireKey = Button("CHANGE", (self.gameManager.SCREENWIDTH / 2 + 20, 255), (160, 40), 0, 0,
                                 [255, 210, 159], [100, 0, 35],
                                 self.gameManager.fonts['title'], [229,64,64], [184, 0, 64], [229,148,57])
        self.changeJumpKey = Button("CHANGE", (self.gameManager.SCREENWIDTH / 2 + 20, 315), (160, 40), 0, 0,
                                    [255, 210, 159], [100, 0, 35],
                                    self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])
        self.changeDashKey = Button("CHANGE", (self.gameManager.SCREENWIDTH / 2 + 20, 380), (160, 40), 0, 0,
                                    [255, 210, 159], [100, 0, 35],
                                    self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])
        self.key_selected = None

    def run(self):
        self.screen.blit(self.gameManager.menuAssets["option"], (0, 0))

        print_text(self.screen, "OPTIONS", (self.gameManager.SCREENWIDTH / 2 - 80, 100), self.gameManager.fonts['title'], color=[0,0,0])

        print_text(self.screen, "FIRE: " + pygame.key.name(self.gameManager.keys["fire"]), (self.gameManager.SCREENWIDTH / 2 - 150, 260),
                   self.gameManager.fonts['title'], color=[0, 0, 0])
        self.changeFireKey.render(self.screen)

        print_text(self.screen, "JUMP: " + pygame.key.name(self.gameManager.keys["jump"]), (self.gameManager.SCREENWIDTH / 2 - 160, 320),
                   self.gameManager.fonts['title'], color=[0, 0, 0])
        self.changeJumpKey.render(self.screen)

        print_text(self.screen, "DASH: " + pygame.key.name(self.gameManager.keys["dash"]), (self.gameManager.SCREENWIDTH / 2 - 150, 380),
                     self.gameManager.fonts['title'], color=[0, 0, 0])
        self.changeDashKey.render(self.screen)

        self.deleteButton.render(self.screen)
        self.backButton.render(self.screen)

        if self.changeFireKey.update():
            self.gameManager.sounds["click"].play()
            self.key_selected = "fire"
        if self.changeJumpKey.update():
            self.gameManager.sounds["click"].play()
            self.key_selected = "jump"
        if self.changeDashKey.update():
            self.gameManager.sounds["click"].play()
            self.key_selected = "dash"

        if self.deleteButton.update():
            self.gameManager.sounds["click"].play()
            try:
                os.remove('save/data.json')
            except FileNotFoundError:
                pass

        if self.backButton.update():
            self.gameManager.sounds["click"].play()
            self.gameManager.changeState("main_menu")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False
            if event.type == pygame.KEYDOWN:
                if self.key_selected:
                    self.gameManager.keys[self.key_selected] = event.key
                    self.key_selected = None