import pygame
from buttonRect import Button


class Intro:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock

        self.nameFont = self.gameManager.fonts["title"]
        self.borderNameFont = self.gameManager.fonts["border"]
        self.textFont = self.gameManager.fonts["big"]

        self.skipButton = Button("SKIP", (1160, 20), (100, 40), 0, 0,
                                    [255, 210, 159], [100, 0, 35],
                                    self.gameManager.fonts['title'], [229, 64, 64], [184, 0, 64], [229, 148, 57])

        pygame.mixer.music.load(self.gameManager.musics["intro"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.03)

        self.sound_played = False

        self.dialogue = [("One day when the GDD club was just playing games as always.", ""),
                         ("...", ""),
                         ("HAVE YOU FINISHED THIS SEMESTER'S GAME YET?", "Yuuka"),
                         ("Uhh... EVERYONE, CODE RED!!!", "Momoi"),
                         ("Oh no you don't, I'm taking you to Sensei.", "Yuuka"),
                         ("NOOOOOOOOOOOOOOOOO... SAVE ME ARISU!!!", "Momoi"),
                         ("ARISU QUEST BEGINS!", "Arisu"),
                         ("No, Arisu, you're going to the Correction Chamber in the mean time.", "Yuuka"),
                         ("And then the quest begins...", "")]
        self.i = 0

    def run(self):
        self.screen.blit(self.gameManager.menuAssets["intro"], (0, 0))

        s = pygame.Surface((1280, 260), pygame.SRCALPHA)
        s.fill((0, 60, 100, 200))
        self.screen.blit(s, (0, 460))
        pygame.draw.rect(self.screen, (255, 255, 255), (40, 459, 1200, 1))

        self.skipButton.render(self.screen)

        if self.skipButton.update():
            self.gameManager.changeState("main_game")

        if not self.sound_played:
            if self.i == 1:
                self.gameManager.sounds["knock"].play()
                self.sound_played = True
            elif self.i == 2:
                self.gameManager.sounds["angry"].play()
                self.sound_played = True
            elif self.i == 5:
                self.gameManager.sounds["kuyashii"].play()
                self.sound_played = True
            elif self.i == 6:
                self.gameManager.sounds["retro_success"].play()
                self.gameManager.sounds["win"].play()
                self.sound_played = True
            elif self.i == 7:
                self.gameManager.sounds["sad"].play()
                self.sound_played = True

        self.render_text(self.dialogue[self.i][1], self.borderNameFont, (38, 428), (0, 0, 0))
        self.render_text(self.dialogue[self.i][1], self.nameFont, (40, 430))
        self.render_text(self.dialogue[self.i][0], self.textFont, (20, 480))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[1] > 60 and pygame.mouse.get_pos()[0] < 1160:
                    self.i += 1
                    self.sound_played = False
                    if self.i == len(self.dialogue):
                        self.gameManager.changeState("main_game")
            if event.type == pygame.MOUSEBUTTONUP:
                pass

    def render_text(self, sentence, font, pos, color=(255, 255, 255)):
        collection = [word.split(' ') for word in sentence.splitlines()]
        space = 9
        x, y = pos
        for line in collection:
            for words in line:
                word_surf, word_rect = font.render(words, color)
                word_width, word_height = word_surf.get_size()
                if x + word_width >= 1280:
                    x = pos[0]
                    y += (word_height + 10)
                self.screen.blit(word_surf, (x, y))
                x += word_width + space
            x = pos[0]
            y += (word_height + 10)