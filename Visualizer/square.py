from pipper import install_packages
install_packages(['pygame', 'euclid3'])

import pygame as pg
import euclid3 as vmath

class Square:
    def __init__(self, pos: vmath.Vector2, size: vmath.Vector2):
        self.pos = pos
        self.size = size
        self.body = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.color = (255, 255, 255)
        self.obstacle = False
        self.start = False
        self.end = False

    def set_color(self, color: list):
        self.color = color

    def draw(self, window):
        pg.draw.rect(window, self.color, (self.pos.x, self.pos.y, self.size.x, self.size.y))

    def mark_obstacle(self):
        self.set_color([0, 0, 0])
        self.obstacle = True

    def mark_start(self):
        self.obstacle = False
        self.start = True
        self.color = (0, 255, 0)

    def mark_end(self):
        self.obstacle = False
        self.end = True
        self.color = (255, 0, 0)

    def reset(self):
        self.obstacle = False
        self.color = (255, 255, 255)
        self.start = False
        self.end = False