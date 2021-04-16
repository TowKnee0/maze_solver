"""
text_box.py
Contains the class allows user input via the keyboard.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""
import pygame


class TextBox:
    """
    A class that creates a TextBox for user input via pygame.

    To enter text, click the textbox, type and press the ENTER key when finished

    Private Instance Attributes:
        - _text: A string that contains the text the user types
        - _default_text: A string that the text box contains by default
        - _clicked: A bool representing if the textbox was clicked
        - _colour: A tuple representing the colour of the textbox when it is not clicked
        - _clicked_colour: A tuple representing the colour of the textbox when it is clicked
        - _surface: A pygame surface that the textbox is drawn on
    """
    _text: str
    _default_text: str
    _background: pygame.Rect
    _clicked: bool
    _colour: tuple[int, int, int]
    _clicked_colour: tuple[int, int, int]
    _surface: pygame.Surface

    def __init__(self, text: str, default_text: str, background: tuple[int, int, int, int],
                 surface: pygame.Surface) -> None:
        """
        Initialize a new TextBox
        """
        self._text = text
        self._default_text = default_text
        self._background = pygame.Rect(background)
        self._surface = surface
        self._clicked = False
        self._colour = (130, 86, 218)
        self._clicked_colour = (239, 50, 50)

    def draw_text_box(self) -> None:
        """
        Draw a TextBox onto _surface
        """
        # Determine what text to draw
        if self._text == '':
            current_text = self._default_text
        else:
            current_text = self._text

        # Draw the text
        text_surface = pygame.font.SysFont('Arial', 16).render(current_text, True,
                                                               (0, 0, 0))

        # Determine what colour to print the background
        if self._clicked:
            pygame.draw.rect(self._surface, self._clicked_colour, self._background)
        else:
            pygame.draw.rect(self._surface, self._colour, self._background)

        self._surface.blit(text_surface, text_surface.get_rect(center=self._background.center))

    def update(self, events: list) -> str:
        """
        Return the value of the string inputted into the text box, and update the object

        If enter has not been pressed, return 'IGNORE' instead. This is just to appease return
        type annotations.
        """

        mouse_position = pygame.mouse.get_pos()

        for event in events:
            # If the text box is clicked, update the corresponding variable
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._background.collidepoint(mouse_position):
                    self._clicked = True
                else:
                    self._clicked = False
            # Add the typed words to self.text
            elif event.type == pygame.KEYDOWN and self._clicked:
                if event.key == pygame.K_RETURN:
                    self._clicked = False
                    return 'mazes/' + self._text
                elif event.key == pygame.K_BACKSPACE:
                    self._text = self._text[0:len(self._text) - 1]
                else:
                    self._text += event.unicode

        return 'IGNORE'
