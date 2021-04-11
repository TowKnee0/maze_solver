"""
main.py:
Contains the main method of the program

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import cv2
import numpy as np
from typing import Tuple
import pygame
from matrix_graph import MatrixGraph
from algorithms import PathfindingAlgorithms
from button import Button, ToggleButton
from image_processing import crop_image

pygame.init()

maze = 'maze3.jpg'

image = cv2.resize(cv2.imread(maze), (1280, 720))

cropped = crop_image(image)

retVal, thresh = cv2.threshold(cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


thinned = np.array(cv2.ximgproc.thinning(thresh)) // 255

# cut borders

# temp = np.delete(thinned, [0, thinned.shape[1] - 1], axis=1)
# temp = np.delete(thinned, [0, thinned.shape[0] - 1], axis=0)


graph1 = MatrixGraph(np.swapaxes(thinned, 0, 1))

# cv2.imshow('t', temp * 255)
# cv2.waitKey(0)

pygame.init()
display = pygame.display.set_mode((1280, 720))
# maze_img = pygame.transform.scale(pygame.image.load(cropped), (1280, 720))
maze_img = pygame.surfarray.make_surface(np.swapaxes(cropped, 0, 1))
display.blit(maze_img, (0, 0))

# surf = pygame.surfarray.make_surface(graph1.graph * 255)
surf = pygame.Surface((1280, 720), pygame.SRCALPHA, 32)
surf = surf.convert_alpha()

display.blit(surf, (0, 0))
alg = PathfindingAlgorithms()

# Initialize the buttons
start_button = ToggleButton((10, 10, 100, 50), 'Start', (0, 170, 0))
end_button = ToggleButton((110, 10, 100, 50), 'End', (170, 0, 0))
restart_button = Button((1000, 10, 100, 50), 'Restart', (255, 0, 0))

# alg.breadth_first_search(graph1, (1212, 709), (393, 432), set(), surf)
# alg.depth_first_search_iterative(graph1, (1212, 709), (393, 432), surf)
start = None
end = None
once = True

while True:
    # print(start, end)
    if start is not None:
        pygame.draw.circle(surf, (0, 255, 0), start, 3)
    if end is not None:
        pygame.draw.circle(surf, (255, 0, 0), end, 3)

    # print(start, end)
    if start is not None and end is not None and once:
        # print(alg.breadth_first_search(graph1, start, end, set(), surf, display))
        print(alg.breadth_first_search(graph1, start, end, set(), surf, display))
        once = False

    # Draw the buttons
    start_button.draw(display)
    end_button.draw(display)
    restart_button.draw(display)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()

            if start_button.active:
                start = start_button.set_pos(graph1, posx, posy)
            start_button.check_pressed(posx, posy)

            if end_button.active:
                end = end_button.set_pos(graph1, posx, posy)
            end_button.check_pressed(posx, posy)

            if restart_button.check_pressed(posx, posy):
                once = True
                start = None
                end = None
                start_button.active = False
                end_button.active = False
                display.blit(maze_img, (0, 0))
                surf.fill((255, 255, 255, 0))

    display.blit(surf, (0, 0))
    pygame.time.wait(1)
    pygame.display.flip()


# cv2.imshow('w', thinned)
#
# cv2.waitKey(0)
