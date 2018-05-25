#!/usr/env/bin python3

import pygame

class Player(object):

    image_front = 'mygame/assets/players/p1_front.png'
    image_right = 'mygame/assets/players/p1_walk.png'
    image_left = 'mygame/assets/players/p1_walk_left.png'
    image_jump = 'mygame/assets/players/p1_jump.png'
    image_down = 'mygame/assets/players/p1_duck.png'
    image_hurt = 'mygame/assets/players/p1_hurt.png'

    image_full_life = 'mygame/assets/players/hud_heartFull.png'
    image_half_life = 'mygame/assets/players/hud_heartHalf.png'
    image_empty_life = 'mygame/assets/players/hud_heartEmpty.png'

    def __init__(self, name, life=5, x=0, y=0, image=image_front, score=0):
        self._name = name
        self._life = life
        self._images_life = []
        self._x = x
        self._y = y
        self._direction = pygame.K_RIGHT
        self._score = score
        self.position = pygame.Rect(x, y, 66, 92)
        self._image = pygame.image.load(image).convert_alpha()
        pygame.display.flip()

    def move_x(self, value):
        if -75 <= (self._x + value) <= 850:
            self._x += value
            self.position = pygame.Rect((75 + self._x), (self._y + 395), 66, 92)

    def move_y(self, value):
        # Other stuff like checking if you a stopped by a plateform in you fall.
        self._y += value
        self.position = pygame.Rect((75 + self._x), (self._y + 395), 66, 92)

    def update(self, event):
        if event.key == pygame.K_LEFT:
            self.move_x(-75)
            self._image = pygame.image.load(self.image_left).convert_alpha()
            self._direction = pygame.K_LEFT
        elif event.key == pygame.K_RIGHT:
            self.move_x(+75)
            self._image = pygame.image.load(self.image_right).convert_alpha()
            self._direction = pygame.K_RIGHT
        elif event.key == pygame.K_UP:
            self.move_y(-90)
            self._image = pygame.image.load(self.image_jump).convert_alpha()
        elif event.key == pygame.K_DOWN:
            self._image = pygame.image.load(self.image_down).convert_alpha()
            self.move_y(+90)
            self._image = pygame.image.load(self.image_front).convert_alpha()

    def always_down(self, sols):
        if self._y <= 15:
            self._image = pygame.image.load(self.image_down).convert_alpha()
            self.move_y(+0.6)
            self._image = pygame.image.load(self.image_front).convert_alpha()

    def update_life(self, value):
        self._life += value
        if self._life == 0:
            self._image = pygame.image.load(self.image_hurt).convert_alpha()

    def update_images_life(self, window, windows_width):
        espace_heart = 60
        for i in range(0, 5):
            if i < self._life:
                image_life = pygame.image.load(self.image_full_life).convert_alpha()
            else:
                image_life = pygame.image.load(self.image_empty_life).convert_alpha()
            window.blit(image_life, (windows_width - espace_heart, 20))
            espace_heart = espace_heart + 60

    def update_score(self, value):
        self._score += value