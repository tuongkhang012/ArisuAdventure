import pygame
import sys
import json

from gameManager import GameManager

if __name__ == '__main__':
    gameManager = GameManager()

    while gameManager.isRunning:
        gameManager.run()

        pygame.display.update()
        gameManager.clock.tick(gameManager.FPS)

    with open('save/data.json', 'w') as f:
        json.dump(gameManager.data, f)
    pygame.quit()
    sys.exit()
