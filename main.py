import pygame

from game.Constants import h, w
from game.Input import get
from game.MainGame import MainGame

pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Flappy Bird")

fps_clock = pygame.time.Clock()
main_game = MainGame(
    screen, bird_type="yellowbird", pipe_type="green", background_type="day"
)

while True:
    main_game.update(get({"ENTER": False, "UP": False, "SPACE": False}))
    pygame.display.update()
    fps_clock.tick(30)
