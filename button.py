import pygame
from typing import Tuple
from matrix_graph import MatrixGraph

class Button:
    def __init__(self, rect: Tuple[int, int, int, int], text: str, color: Tuple[int, int, int]):
        self.rect = rect
        self.text = text
        self.color = color
        self.text_surface = pygame.font.SysFont('Arial', 20).render(self.text, False, (0, 0, 0))
        self.text_pos = self._compute_text_location()

    def _compute_text_location(self) -> Tuple[int, int]:
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()

        x_pos = (self.rect[0] + self.rect[2] // 2) - text_w // 2
        y_pos = (self.rect[1] + self.rect[3] // 2) - text_h // 2
        return (x_pos, y_pos)

    def draw(self, display: pygame.display) -> None:
        pygame.draw.rect(display, self.color, self.rect)
        display.blit(self.text_surface, self.text_pos)

    def check_pressed(self, posx: int, posy: int):
        pyrect = pygame.Rect(self.rect)
        if pyrect.collidepoint(posx, posy):
            return True
        else:
            return False


class ToggleButton(Button):
    def __init__(self, rect: Tuple[int, int, int, int], text: str, color: Tuple[int, int, int]):
        Button.__init__(self, rect, text, color)
        self.active = False

    def check_pressed(self, posx: int, posy: int):
        pyrect = pygame.Rect(self.rect)
        if pyrect.collidepoint(posx, posy):
            self.active = not self.active
        else:
            self.active = False

    def draw(self, display: pygame.display) -> None:
        if self.active:
            color = (self.color[0], self.color[1], self.color[2] + 255)
        else:
            color = self.color
        pygame.draw.rect(display, color, self.rect)
        display.blit(self.text_surface, self.text_pos)

    def set_pos(self, graph: MatrixGraph, posx, posy):
        if self.active:
            try:
                return graph.closest_path((posx, posy), 5)
            except Exception:
                print('Select point closer to path')
                return None
