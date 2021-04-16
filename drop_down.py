"""
drop_down.py:
Contains the DownDown class that generates a drop down menu for the program

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

from typing import Any, Union
import pygame


class DropDown:
    """
    A class used to generate a dropdown menu

    Private Instance Attributes:
        - _active: Tuple of colors used to be the background for the active item
        - _not_active: Tuple of colors used to be the background for the non-active items
        - _dropped: Bool representing if the list is dropped down
        - _hovered: Bool representing if the first entry of the list has been hovered over
        - _items: A list of items representing what is in the drop down list
        - _rectangle: The (x, y, w, h) of the background rectangle

    Sample Usage:
    >>> my_drop_down = DropDown(['item1', 'item2',], (200, 200, 5, 5), pygame.Surface((1280, 720)))
    """

    _active: tuple[int, int, int] = (70, 158, 236)  # RGB: Baby Blue
    _not_active: tuple[int, int, int] = (182, 188, 192)  # RGB: Grey
    _dropped: bool = False
    _hovered: Union[int, bool] = False
    _surface: pygame.Surface
    _items: list[Any]
    _rectangle: tuple[int, int, int, int]

    def __init__(self, items: list[Any], rectangle: tuple[int, int, int, int],
                 surface: pygame.Surface) -> None:
        """
        Initialize a new DropDown menu
        """
        self._items = items
        self._rectangle = rectangle
        self._surface = surface

    def draw_list(self) -> None:
        """
        Draw the dropdown list
        """
        # Rectangle used as a background
        x, y, w, h = self._rectangle
        menu_rectangle = pygame.Rect(x, y, w, h)

        # Draw the rectangle and the text
        pygame.draw.rect(self._surface, self._active, menu_rectangle)
        text_surface = pygame.font.SysFont('Arial', 20).render(self._items[0],
                                                               True, (0, 0, 0))
        self._surface.blit(text_surface, text_surface.get_rect(center=menu_rectangle.center))

        # If the list is dropped down, draw the other items as well
        if self._dropped:
            for i in range(1, len(self._items)):
                new_y = y + (i * h)
                new_rect = pygame.Rect(x, new_y, w, h)
                pygame.draw.rect(self._surface, self._not_active, new_rect)
                new_text_surface = pygame.font.SysFont('Arial', 20).render(self._items[i],
                                                                           True, (0, 0, 0))
                self._surface.blit(new_text_surface,
                                   new_text_surface.get_rect(center=new_rect.center))

    def update(self, events: list) -> int:
        """
        Return the selected option of the dropdown menu.

        Update the menu depending if it is dropped or not
        """

        # Check if the first item is hovered over
        x, y, w, h = self._rectangle
        first_rect = pygame.Rect(self._rectangle)
        mouse_position = pygame.mouse.get_pos()
        self._hovered = first_rect.collidepoint(mouse_position)

        selected_option = -1

        # Check all items to see if they are hovered over
        for i in range(0, len(self._items)):
            collision_rect = pygame.Rect(x, y + (i * h), w, h)
            if collision_rect.collidepoint(mouse_position):
                selected_option = i
                break

        # If nothing is clicked, make the list undropped
        if selected_option == -1:
            self._dropped = False

        # If the items in the list are clicked, return what number option it was
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._hovered:
                    self._dropped = not self._dropped
                elif self._dropped and selected_option >= 0:
                    self._dropped = False
                    return selected_option
        return -1

    def update_list(self, swap: int) -> None:
        """
        Update the list to swap the clicked index with the first index
        """
        self._items[0], self._items[swap] = self._items[swap], self._items[0]

    def get_first(self) -> Any:
        """
        Return the first item in the item list
        """
        return self._items[0]


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['pygame', 'typing'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
