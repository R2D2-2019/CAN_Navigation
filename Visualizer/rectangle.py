from pipper import install_packages
install_packages(['pygame'])

import pygame as pg

class Rectangle(pg.sprite.Sprite):
    """
    Square shape used in our AStar visualization. Provides an easy way to draw a rectangle shape using pygame.
    Inherits from pygame sprite to pack them into a group later on.
    """
    def __init__(self, pos: list, size: list):
        """
        Default and only constructor.
        :param pos: list that contains the x and y coordinates
        :param size: list that contains the width and height
        """
        super().__init__()
        self.image = pg.Surface([size[0], size[1]])
        self.color = (255, 255, 255)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.obstacle = False
        self.start = False
        self.end = False

    def set_color(self, color: list):
        """ sets the rectangle color. """
        self.color = color
        self.image.fill(self.color)

    def mark_obstacle(self):
        """ Marks the rectangle as obstacle and changes the color.  """
        self.set_color([0, 0, 0])
        self.obstacle = True

    def mark_start(self):
        """ Marks the rectangle as the start cell and changes the color. """
        self.obstacle = False
        self.start = True
        self.set_color((0, 255, 0))

    def mark_end(self):
        """ Marks the rectangle as the end cell and changes the color. """
        self.obstacle = False
        self.end = True
        self.set_color((255, 0, 0))

    def reset(self):
        """ Resets the  variables so it can be used again for pathfinding. """
        self.obstacle = False
        self.set_color((255, 255, 255))
        self.start = False
        self.end = False
