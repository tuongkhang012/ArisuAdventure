import pygame


class Button:

    def __init__(self, text, pos, size, margin_x, margin_y, color, textcolor,
                 font, hovercolor=None, presscolor=None, border=None):
        """
        Create a Button object

        :param text: Text for the button
        :param x: x-coordinate for the button
        :param y: y-coordinate for the button
        :param width: the width of the button
        :param height: the height of the button
        :param margin_x: the margin_x for the text
        :param margin_y: the margin_y for the text
        :param color: the color of the button
        :param textcolor: the color of the text
        :param font: the font used
        """
        self.font = font
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.text = text
        self.textcolor = textcolor

        if not hovercolor:
            self.hovercolor = self.textcolor
        else:
            self.hovercolor = hovercolor

        if not presscolor:
            self.presscolor = self.textcolor
        else:
            self.presscolor = presscolor

        if not border:
            self.border = 0
        else:
            self.border_color = border

        self.marginx = margin_x
        self.marginy = margin_y
        self.clicked = False

    def render(self, surface):
        """
        Draw the button while return a bool to detect click

        :param surface: the display to draw the button on
        :return: a boolean for click
        """

        action = False
        pos = pygame.mouse.get_pos()
        color = self.textcolor

        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        if rect.collidepoint(pos):
            color = self.hovercolor
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                color = self.presscolor
                self.clicked = True

        text_surf, text_rect = self.font.render(self.text, color)
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        pygame.draw.rect(surface, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 3)
        surface.blit(text_surf, (self.pos[0] + self.marginx + self.size[0]/2 - text_rect.w / 2,
                                 self.pos[1] + self.marginy + self.size[1]/2 - text_rect.h / 2))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def update(self):
        return self.clicked
