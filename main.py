import pygame
import sys

from gameManager import GameManager

if __name__ == '__main__':
    gameManager = GameManager()

    while gameManager.isRunning:
        gameManager.run()

        pygame.display.update()
        gameManager.clock.tick(gameManager.FPS)

    pygame.quit()
    sys.exit()
