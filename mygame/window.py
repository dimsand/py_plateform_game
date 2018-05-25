#!/usr/env/bin python3

import pygame
import time

from mygame.player import Player
from mygame.enemy import Enemy
from mygame.laser import Laser
from pygame.locals import *


class Window(object):
    image_icone = 'mygame/assets/players/p1_front.png'
    image_bg = 'mygame/assets/bg.png'
    img_grass = 'mygame/assets/tiles/grass.png'

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    clock = None
    _enemies = None
    _sols = []
    _lasers = []
    _enemy_touche = None
    player = None

    def __init__(self, width=1000, height=600):
        self._width = width
        self._height = height

        pygame.init()
        self.menu_showed = True
        self.pause = False
        self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption('Plateform Game')
        icone = pygame.image.load(self.image_icone)
        pygame.display.set_icon(icone)

        self.init_screen()

        pygame.key.set_repeat(400, 30)

        pygame.display.flip()

    def init_screen(self):
        self.clock = time.clock()

        self.draw_bg()
        self.draw_sol()

        self._enemies = []
        self._lasers = []
        self._sols = []

        self.draw_new_enemy()

        self.player = Player('Dimitri', 5, 10, 15)
        self._window.fill(Color("green"), self.player.position)
        self._window.blit(self.player._image, (75 + self.player._x, (self._height - 190)))
        self.player.update_images_life(self._window, self._width)

    def draw_bg(self):
        fond = pygame.image.load(self.image_bg).convert()
        for y in range(0, self._height, 256):
            for x in range(0, self._width, 256):
                self._window.blit(fond, (x, y))

    def draw_sol(self):
        grass = pygame.image.load(self.img_grass).convert_alpha()
        for x in range(0, self._width, 70):
            self._window.blit(grass, (x, (self._height - 100)))

    def draw_new_enemy(self):
        enemy = Enemy((self._width - 20), (self._height - 128))
        self._enemies.append(enemy)

    def draw_enemies(self):
        for enemy in self._enemies:
            enemy.update(pygame.K_LEFT)
            self._window.blit(enemy._img, (enemy._x, enemy._y))

    def new_laser(self):
        laser = Laser((75 + self.player._x), (self.player._y + 430), self.player._direction)
        self._lasers.append(laser)

    def draw_lasers(self):
        for laser in self._lasers:
            laser.update()
            self._window.blit(laser._img, (laser._x, laser._y))

    def write_score(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render(str(self.player._score), False, self.GREEN)
        self._window.blit(textsurface, (5, 5))

    def check_colision(self):
        touche = False
        for enemy in self._enemies:
            if self._enemy_touche != enemy:
                if self.player.position.colliderect(enemy.position):
                    touche = True
                    self._enemy_touche = enemy
                    break
        if touche:
            self.player.update_life(-1)

    def check_enemies_dead(self):
        for laser in self._lasers:
            for enemy in self._enemies:
                if laser.position.colliderect(enemy.position):
                    self._enemies.remove(enemy)
                    self._lasers.remove(laser)
                    self.player.update_score(+1)
                    break

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text_title, font_size, color, small_title=''):
        largeText = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(text_title, largeText, color)
        if small_title != '':
            littleText = pygame.font.Font('freesansbold.ttf', font_size - 30)
            TextSurf2, TextRect2 = self.text_objects(small_title, littleText, color)
            TextRect.center = ((self._width / 2), (self._height / 4))
            TextRect2.center = ((self._width / 2), (self._height / 2))
            self._window.blit(TextSurf2, TextRect2)
        else:
            TextRect.center = ((self._width / 2), (self._height / 2))
        self._window.blit(TextSurf, TextRect)

    def show_menu(self):
        self._window.fill((231, 232, 241, 0.5))
        if self.player._life == 0:
            self.message_display('Game over', 100, self.RED, 'Press Escape for new game')
        elif self.pause:
            self.message_display('Pause', 95, self.WHITE, 'Press Space to back to game')
        else:
            self.message_display('Platform Game', 115, self.BLACK, 'Press Space to game')

    def run(self):
        running = True
        time_enemies = 0
        while running:

            if not self.menu_showed:
                self.draw_bg()
                self.draw_sol()

                self.draw_enemies()

                if time_enemies != int(self.clock + time.clock()):
                    time_enemies = int(self.clock + time.clock())
                    if time_enemies % 10 == 0:
                        self.draw_new_enemy()

                self.player.always_down(self._sols)

                self.draw_lasers()

                self.check_enemies_dead()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.menu_showed = True
                            self.pause = True
                        if event.key in [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                            self.player.update(event)
                        if event.key == pygame.K_SPACE:
                            self.new_laser()

                self._window.blit(self.player._image, (75 + self.player._x, ((self._height - 205) + self.player._y)))
                self.player.update_images_life(self._window, self._width)

                self.check_colision()

                if self.player._life == 0:
                    self.menu_showed = True
                    self.pause = False
                    self.show_menu()

            elif self.player._life == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.init_screen()
            else:
                self.show_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.menu_showed = False
                            self.pause = False

            self.write_score()

            pygame.display.flip()
