"""
button.py:
Contains two button methods used with pygame.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import pygame
from typing import Tuple
from matrix_graph import MatrixGraph


class Button:
    """
    A class that creates a pygame button.

    Private Instance Attributes:
        - _rect: A tuple that stores the (left, top, width, height) used to draw a pygame rectangle
        - _text: A string that stores the text of the button
        - _color: A tuple that stores the color the button in RGB (r,g,b)
        - _text_pos: A tuple that stores the location of the text location
    """
    _rect: tuple
    _text: str
    _color: tuple
    _text_surface: pygame.Surface
    _text_pos: tuple

    def __init__(self, rect: tuple[int, int, int, int], text: str, color: tuple[int, int, int]):
        """
        Initialize a new button
        """
        self._rect = rect
        self._text = text
        self._color = color
        self._text_surface = pygame.font.SysFont('Arial', 20).render(self._text, True, (0, 0, 0))
        self._text_pos = self._compute_text_location()

    def _compute_text_location(self) -> tuple[int, int]:
        """
        Return a tuple that contains the (x,y) locations of the text location
        """
        text_w = self._text_surface.get_width()
        text_h = self._text_surface.get_height()

        x_pos = (self._rect[0] + self._rect[2] // 2) - text_w // 2
        y_pos = (self._rect[1] + self._rect[3] // 2) - text_h // 2
        return (x_pos, y_pos)

    def draw(self, display: pygame.display) -> None:
        """
        A function used to draw a button
        """
        pygame.draw.rect(display, self._color, self._rect)
        display.blit(self._text_surface, self._text_pos)

    def check_pressed(self, posx: int, posy: int) -> bool:
        """
        Return True if the button has been pressed, return False otherwise
        """
        pyrect = pygame.Rect(self._rect)
        if pyrect.collidepoint(posx, posy):
            return True
        else:
            return False


class ToggleButton(Button):
    """
    A child of Button. This class is creates a button with a toggle feature

    Private Instance Attributes:
        - rect: A tuple that stores the (left, top, width, height) used to draw a pygame rectangle
        - text: A string that stores the text of the button
        - color: A tuple that stores the color the button in RGB (r,g,b)
        - text_pos: A tuple that stores the location of the text location

    Public Instance Attributes:
        - active: A bool that represents if the button is toggled
    """

    active: bool

    def __init__(self, rect: Tuple[int, int, int, int], text: str, color: Tuple[int, int, int]):
        """
        Initialize a new toggle button
        """
        Button.__init__(self, rect, text, color)
        self.active = False

    def check_pressed(self, posx: int, posy: int) -> None:
        """
        Check if the button is currently toggled
        """
        pyrect = pygame.Rect(self._rect)
        if pyrect.collidepoint(posx, posy):
            self.active = not self.active
        else:
            self.active = False

    def draw(self, display: pygame.display) -> None:
        """
        A function used to draw a button
        """
        if self.active:
            color = (self._color[0], self._color[1], self._color[2] + 255)
        else:
            color = self._color
        pygame.draw.rect(display, color, self._rect)
        display.blit(self._text_surface, self._text_pos)

    def set_pos(self, graph: MatrixGraph, posx, posy):
        """
        Set the position of the button to be the closest on the path. If the point is too far
        print an error message
        """
        if self.active:
            try:
                return graph.closest_path((posx, posy), 5)
            except Exception:
                print('Select point closer to path')
                return None
