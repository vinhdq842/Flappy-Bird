import pygame

from game.Constants import w, h
from game.MainGame import MainGame

pygame.init()

screen = pygame.display.set_mode((w, h))

fps_clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

running = True
main_game = MainGame(screen)

while running:
    main_game.update()
    pygame.display.flip()

    fps_clock.tick(30)
pygame.quit()
