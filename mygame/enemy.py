#!/usr/env/bin python3

import pygame
import random


class Enemy(object):

    type_enemies = ['slimeWalk1.png', 'snailWalk1.png']

    def __init__(self, x=0, y=0, img=type_enemies[random.randrange(0, 2)]):
        self._x = x
        self._y = y
        self._img = pygame.image.load('mygame/assets/enemies/' + img).convert_alpha()
        self.position = pygame.Rect(x, y, 50, 28)
        pygame.display.flip()

    def move_x(self, value):
        # Other stuff like checking if you are running into a wall
        self._x += value
        self.position = pygame.Rect(self._x, self._y, 50, 28)

    def move_y(self, value):
        # Other stuff like checking if you a stopped by a plateform in you fall.
        self._y += value
        self.position = pygame.Rect(self._x, self._y, 50, 28)

    def update(self, event):
        if event == pygame.K_RIGHT:
            self.move_x(+0.1)
        elif event == pygame.K_LEFT:
            self.move_x(-0.1)
