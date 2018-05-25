#!/usr/env/bin python3

import pygame
import random


class Laser(object):

    def __init__(self, x=0, y=0, direction=pygame.K_RIGHT):
        self._x = x
        self._y = y
        self._direction = direction
        self._img = pygame.image.load('mygame/assets/items/fireball.png').convert_alpha()
        self.position = pygame.Rect(x, y, 70, 70)
        pygame.display.flip()

    def move_x(self, value):
        # Other stuff like checking if you are running into a wall
        self._x += value
        self.position = pygame.Rect(self._x, self._y, 70, 70)

    def move_y(self, value):
        # Other stuff like checking if you a stopped by a plateform in you fall.
        self._y += value
        self.position = pygame.Rect(self._x, self._y, 70, 70)

    def update(self):
        if self._direction == pygame.K_RIGHT:
            self.move_x(+1.2)
        elif self._direction == pygame.K_LEFT:
            self.move_x(-1.2)
