import math
import random

import pygame

from game.Background import Background
from game.Base import Base
from game.Bird import Bird
from game.Constants import w, h, NUM_PIPES, HORIZONTAL_SPACE
from game.Input import get
from game.NumberDrawer import NumberDrawer
from game.Pipe import Pipe
from game.SoundPlayer import SoundPlayer


class MainGame:

    def __init__(self, screen):
        self.screen = screen
        self.message = pygame.image.load("game/images/message.png")
        self.message_alpha = 1.0
        self.point = 0
        self.over_image = pygame.image.load("game/images/game-over.png")
        self.restart_button = pygame.image.load("game/images/restart.png")
        self.pipes = []
        self.game_status = 0
        self.bird_type = 2
        self.pipe_type = 0
        self.bg_type = 0
        self.white_screen = False
        self.background = Background(self)
        self.base = Base(self)
        self.bird = Bird(self)
        self.number = NumberDrawer()
        self.key = {"ENTER": False, "UP": False, "SPACE": False}
        self.initialize_pipe()
        self.sound_player = SoundPlayer()

    def initialize_pipe(self):
        self.pipes.clear()
        for i in range(NUM_PIPES):
            self.add_pipe()

    def add_pipe(self):
        pipe = Pipe(self,
                    (self.pipes[len(self.pipes) - 1].x if len(self.pipes) > 0 else w) + HORIZONTAL_SPACE + 52,
                    math.floor(random.random() * 120) + h / 2 - 140)
        self.pipes.append(pipe)

    def reset_game(self):
        self.game_status = 0
        self.initialize_pipe()
        self.message_alpha = 1.0
        self.point = 0
        self.bird = Bird(self)
        self.white_screen = False
        self.sound_player.swoosh_sound.play_sound()

    def paint(self):
        self.background.render()

        if self.game_status > 0:
            for pipe in self.pipes:
                pipe.render()
                if self.game_status == 1:
                    pipe.move()

        self.update_pipes()
        self.base.render()
        if self.game_status < 2:
            self.base.move()

        self.number.draw_number(str(self.point), w / 2 - self.number.string_width(str(self.point)) / 2, 10, self.screen)

        self.show_message()
        self.bird.render()
        self.check_collision()
        self.update_point()

        if self.game_status == 2:
            if not self.white_screen:
                self.screen.fill((255, 255, 255))
                self.white_screen = True

            self.show_over_image()

    def update(self):
        self.key = get({"ENTER": False, "UP": False, "SPACE": False})
        self.move()
        self.paint()

    def move(self):
        if self.key["ENTER"] or self.key["UP"] or self.key["SPACE"]:
            if self.game_status == 0:
                self.game_status = 1
                self.bird.keep_flapping = False
            elif self.game_status == 1:
                if self.bird.y > -self.bird.get_height():
                    self.sound_player.wing_sound.play_sound()
                    self.bird.angle = -math.pi / 8
                    self.bird.speed = -6
                    self.bird.y += self.bird.speed
            elif self.game_status == 2 and self.key["ENTER"]:
                self.reset_game()
        self.key = {"ENTER": False, "UP": False, "SPACE": False}

    def update_point(self):
        if self.game_status == 1:
            for pipe in self.pipes:
                check = self.bird.x + self.bird.get_width() / 2 - pipe.x

                if pipe.speed_x > check > 0:
                    self.point += 1
                    self.sound_player.point_sound.play_sound()

    def update_pipes(self):
        if len(self.pipes) > 0:
            if self.pipes[0].x < -self.pipes[0].get_width():
                self.pipes.remove(self.pipes[0])
                self.add_pipe()

    def check_collision(self):
        if self.game_status == 2:
            return

        for pipe in self.pipes:
            if (
                    self.bird.x + self.bird.get_width() / 2 >= pipe.x and self.bird.x - self.bird.get_width() / 2 <= pipe.x + pipe.get_width()) \
                    and \
                    (
                            self.bird.y - self.bird.get_height() / 2 <= pipe.y or self.bird.y + self.bird.get_height() / 2 - 9 >= pipe.y + pipe.space):

                if pipe.x - self.bird.get_width() / 2 + 2 < self.bird.x < pipe.x + pipe.get_width() - self.bird.get_width() / 2 - 2:
                    if self.bird.y - self.bird.get_height() / 2 <= pipe.y:
                        self.bird.y = self.bird.get_height() / 2 + pipe.y

                    if self.bird.y + self.bird.get_height() / 2 - 9 >= pipe.y + pipe.space:
                        self.bird.y = -self.bird.get_height() / 2 + pipe.y + pipe.space

                self.sound_player.hit_sound.play_sound()
                self.game_status = 2
                self.bird.speed = 8

    def show_message(self):
        if self.message_alpha <= 0.0:
            return

        if self.message_alpha > 0.0 and self.game_status == 1:
            self.message_alpha -= 0.05 if self.message_alpha > 0.05 else self.message_alpha

        tmp = pygame.Surface((w, h)).convert()
        tmp.blit(self.screen, (0, 0))
        tmp.blit(self.message, (w / 2 - self.message.get_width() / 2, h / 2 - self.message.get_height() / 2))
        tmp.set_alpha(int(self.message_alpha * 255))
        self.screen.blit(tmp, (0, 0))

    def show_over_image(self):
        self.screen.blit(self.over_image, (w / 2 - self.over_image.get_width() / 2, h / 5))
        self.screen.blit(self.restart_button, (w / 2 - self.restart_button.get_width() / 2, h / 2))
