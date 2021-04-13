"""
timer.py
Contains the class that tracks the amount of time that the pathfinding algorithms take.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import pygame


class Timer:
    """
    A class that tracks the amount of time that has passed

    Instance Attributes:
        - clock: A pygame clock object
        - milliseconds: An integer that represents how many milliseconds have passed
        - seconds: An integer that represents how many seconds have passed
        - minutes: An integer that represents how many minutes have passed

    """

    clock: pygame.time.Clock
    milliseconds: int
    seconds: int
    minutes: int

    def __init__(self) -> None:
        """
        Initialize a pygame clock
        """
        self.clock = pygame.time.Clock()
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.update_time()

    def update_time(self) -> None:
        """
        Update the various time attributes
        """
        self.milliseconds += self.clock.tick_busy_loop()
        self.seconds = self.milliseconds // 1000
        self.minutes = self.seconds // 60

    def get_time(self) -> tuple[int, int, int]:
        """
        Return a tuple of integers that correspond to (milliseconds, seconds, minutes)
        """
        return (self.milliseconds, self.seconds, self.minutes)

    def get_text_surface(self) -> pygame.Surface:
        """
        Get the python surface with the current time
        """
        mi = self.milliseconds % 1000 // 10
        s = self.seconds % 60
        m = self.minutes
        if mi < 10:
            mi = f'0{mi}'
        if s < 10:
            s = f'0{s}'
        if m < 10:
            m = f'0{m}'
        string = f'TIMER: {m}:{s}:{mi}'
        text_surface = pygame.font.SysFont('Arial', 20).render(string, True, (0, 0, 0))
        return text_surface
