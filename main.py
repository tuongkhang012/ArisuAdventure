import pygame, sys
from gameManager import GameManager

if __name__ == '__main__':
    gameManager = GameManager()

    while gameManager.isRunning:
        gameManager.run()
        gameManager.clock.tick(gameManager.FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
