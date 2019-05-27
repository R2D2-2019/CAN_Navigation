from pipper import install_packages
install_packages(['pygame', 'euclid3'])

import pygame as pg
import euclid3 as vmath

class Drawable:
    """
    Abstract class only for overriding by a child class.
    """
    def __init__(self):
        pass
    
    def draw(self, window):
        pass

class Square(Drawable):
    """
    Square shape used in our AStar visualization. Provides an easy way to draw a rectangle shape using pygame.
    Uses the euclid3 module for vector2.
    """
    def __init__(self, pos: vmath.Vector2, size: vmath.Vector2):
        """
        Default and only constructor.
        :param pos: euclid3 vector2 for window position.
        :param size: euclid3 vector2 for size in pixels.
        """
        Drawable.__init__(self)
        self.pos = pos
        self.size = size
        self.body = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.color = (255, 255, 255)

        self.obstacle = False
        self.start = False
        self.end = False

    def draw(self, window):
        """ override from base class. """
        pg.draw.rect(window, self.color, (self.pos.x, self.pos.y, self.size.x, self.size.y))

    def set_color(self, color: list):
        """ sets the rectangle color. """
        self.color = color

    def mark_obstacle(self):
        """ Marks the rectangle as obstacle and changes the color.  """
        self.set_color([0, 0, 0])
        self.obstacle = True

    def mark_start(self):
        """ Marks the rectangle as the start cell and changes the color. """
        self.obstacle = False
        self.start = True
        self.color = (0, 255, 0)

    def mark_end(self):
        """ Marks the rectangle as the end cell and changes the color. """
        self.obstacle = False
        self.end = True
        self.color = (255, 0, 0)

    def reset(self):
        """ Resets the  variables so it can be used again for pathfinding. """
        self.obstacle = False
        self.color = (255, 255, 255)
        self.start = False
        self.end = False