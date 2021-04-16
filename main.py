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
from drop_down import DropDown
from button import Button, ToggleButton
from text_box import TextBox
from image_processing import crop_image

# Constants
GUI_Y_OFFSET = 50  # The offset used for the GUI at the top of the program
PADDING_Y = round(.3 * 720)
PADDING_X = round(.10 * 1280)


# LEGACY CODE I DO NOT WANT TO DELETE YET IN CASE I MESSED SOMETHING UP
# ___________________________________________

# pygame.init()
#
# maze = 'maze3.jpg'
#
# image = cv2.resize(cv2.imread(maze), (1280, 720))
#
# cropped = crop_image(image)
#
# retVal, thresh = cv2.threshold(cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#
# thinned = np.array(cv2.ximgproc.thinning(thresh)) // 255
#
# # cut borders
#
# # temp = np.delete(thinned, [0, thinned.shape[1] - 1], axis=1)
# # temp = np.delete(thinned, [0, thinned.shape[0] - 1], axis=0)
#
#
# graph1 = MatrixGraph(np.swapaxes(thinned, 0, 1))
#
# # cv2.imshow('t', temp * 255)
# # cv2.waitKey(0)
#
# pygame.init()
# display = pygame.display.set_mode((1280 + PADDING_X, 720 + GUI_Y_OFFSET + PADDING_Y))
# # maze_img = pygame.transform.scale(pygame.image.load(cropped), (1280, 720))
# maze_img = pygame.surfarray.make_surface(np.swapaxes(cropped, 0, 1))
#
# # Center the maze image
# maze_img_w = maze_img.get_width()
# maze_img_h = maze_img.get_height()
#
# surface_w = display.get_width()
# surface_h = display.get_height()
#
# centered_w = ((surface_w - maze_img_w) // 2)
# centered_h = ((surface_h - maze_img_h) // 2) + GUI_Y_OFFSET
#
# display.blit(maze_img, (centered_w, centered_h))
#
# # surf = pygame.surfarray.make_surface(graph1.graph * 255)
# surf = pygame.Surface((1280 + PADDING_X, 720 + GUI_Y_OFFSET + PADDING_Y), pygame.SRCALPHA, 32)
# surf = surf.convert_alpha()
#
# display.blit(surf, (0, 0))

# ___________________________________________

def initialize_maze(maze_path: str, rectangular: bool = True) -> tuple[
                                                                    pygame.Surface, pygame.Surface,
                                                                    MatrixGraph, pygame.Surface,
                                                                    int, int, None, None, bool]:

    """
    Initialize the program variables with respect to the maze found at maze_path.

    Return a tuple containing: (The Pygame Display, The Surface to draw on, The MatrixGraph for the
    maze, The MatrixGraph Surface layer, The amount of pixels used to center the width, The amount
    of pixels used to center the height, A None value representing the start of the maze, A None
    value representing the end of the maze, and a bool representing if we can run the program once)
    """

    pygame.init()

    maze = maze_path

    image = cv2.resize(cv2.imread(maze), (1280, 720))

    # crop only works for rectangular mazes
    if rectangular:
        cropped = crop_image(image)
    else:
        cropped = image

    # Global thresholding using Otsu's binarization
    retVal, thresh = cv2.threshold(cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY), 0, 255,
                                   cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    thinned = np.array(cv2.ximgproc.thinning(thresh)) // 255

    # cut borders

    if not rectangular:
        temp = np.delete(thinned, [0, thinned.shape[1] - 1], axis=1)
        temp = np.delete(thinned, [0, thinned.shape[0] - 1], axis=0)
        graph = MatrixGraph(np.swapaxes(temp, 0, 1))
    else:
        graph = MatrixGraph(np.swapaxes(thinned, 0, 1))

    pygame.init()
    display_surface = pygame.display.set_mode((1280 + PADDING_X, 720 + GUI_Y_OFFSET + PADDING_Y))
    # maze_img = pygame.transform.scale(pygame.image.load(cropped), (1280, 720))
    maze_surface = pygame.surfarray.make_surface(np.swapaxes(cropped, 0, 1))

    # Center the maze image
    maze_img_w = maze_surface.get_width()
    maze_img_h = maze_surface.get_height()

    surface_w = display_surface.get_width()
    surface_h = display_surface.get_height()

    maze_centered_width = ((surface_w - maze_img_w) // 2)
    maze_centered_height = ((surface_h - maze_img_h) // 2) + GUI_Y_OFFSET

    display_surface.blit(maze_surface, (maze_centered_width, maze_centered_height))

    # surf = pygame.surfarray.make_surface(graph1.graph * 255)
    surface = pygame.Surface((1280 + PADDING_X, 720 + GUI_Y_OFFSET + PADDING_Y), pygame.SRCALPHA,
                             32)
    surface = surface.convert_alpha()

    display_surface.blit(surface, (0, 0))

    start_vertex = None
    end_vertex = None
    run_once = True

    return (
        display_surface, surface, graph, maze_surface, maze_centered_width, maze_centered_height,
        start_vertex, end_vertex, run_once)


# Initialize variables from the initialize_maze call with the specified maze
display, surf, graph1, maze_img, \
    centered_w, centered_h, start, end, once = initialize_maze('mazes/maze.png')

# Initialize the GUI. This includes buttons, text boxes, drop down menus, timers, and counters.
start_button = ToggleButton((10, 10, 100, 50), 'Start', (0, 170, 0))
end_button = ToggleButton((110, 10, 100, 50), 'End', (170, 0, 0))
restart_button = Button((620, 10, 100, 50), 'Restart', (255, 0, 0))
iteration_counter_pos = (210, 10)
timer_pos = (210, 30)  # 412
algo_drop_down = DropDown(['Breadth First Search', 'Depth First Search', 'A*'],
                          (420, 10, 200, 50), display)
maze_drop_down = DropDown(['Maze 1', 'Maze 2', 'Maze 3', 'Other'], (720, 10, 200, 50), display)
maze_drop_down_text_box = TextBox('', 'Enter File Name', (925, 10, 150, 50), display)
draw_text_box = False

# Initialize the algorithm object
alg = PathfindingAlgorithms(iteration_counter_pos, centered_w, centered_h, timer_pos)

# alg.breadth_first_search(graph1, (1212, 709), (393, 432), set(), surf)
# alg.depth_first_search_iterative(graph1, (1212, 709), (393, 432), surf)

while True:
    if start is not None:
        pygame.draw.circle(surf, (0, 255, 0), (start[0] + centered_w, start[1] + centered_h), 3)
    if end is not None:
        pygame.draw.circle(surf, (255, 0, 0), (end[0] + centered_w, end[1] + centered_h), 3)

    if start is not None and end is not None and once:
        if algo_drop_down.get_first() == 'Breadth First Search':
            alg.breadth_first_search(graph1, start, end, surf, display)
        elif algo_drop_down.get_first() == 'Depth First Search':
            alg.depth_first_search_iterative(graph1, start, end, surf, display)
        else:
            alg.a_star(graph1, start, end, surf, display)  # A STAR
        once = False

    # Redraw the background and maze, then draw the buttons
    display.fill((255, 255, 255, 0))
    display.blit(maze_img, (centered_w, centered_h))
    start_button.draw(display)
    end_button.draw(display)
    restart_button.draw(display)
    algo_drop_down.draw_list()
    maze_drop_down.draw_list()
    if draw_text_box:
        maze_drop_down_text_box.draw_text_box()

    # Check pygame events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()

            if start_button.active:
                start = start_button.set_pos(graph1, posx - centered_w, posy - centered_h)
            start_button.check_pressed(posx, posy)

            if end_button.active:
                end = end_button.set_pos(graph1, posx - centered_w, posy - centered_h)
            end_button.check_pressed(posx, posy)

            if restart_button.check_pressed(posx, posy):
                once = True
                start = None
                end = None
                start_button.active = False
                end_button.active = False
                display.blit(maze_img, (centered_w, centered_h))
                surf.fill((255, 255, 255, 0))

    # Update the algorithm drop down list
    algo_drop_down_selected = algo_drop_down.update(events)
    if algo_drop_down_selected != -1:
        algo_drop_down.update_list(algo_drop_down_selected)

    # Update the selected maze drop down list
    maze_drop_down_selected = maze_drop_down.update(events)
    if maze_drop_down_selected != -1:
        maze_drop_down.update_list(maze_drop_down_selected)

        # Check the selected option
        if maze_drop_down.get_first() == 'Maze 1':
            # Reassign variables with respect to the new maze
            display, surf, graph1, maze_img, \
                centered_w, centered_h, start, end, once = initialize_maze('mazes/maze.png')
            alg.update_off_set_values(centered_w, centered_h)
            draw_text_box = False
        elif maze_drop_down.get_first() == 'Maze 2':
            # Reassign variables with respect to the new maze
            display, surf, graph1, maze_img, \
                centered_w, centered_h, start, end, once = initialize_maze('mazes/maze2.jpg')
            alg.update_off_set_values(centered_w, centered_h)
            draw_text_box = False
        elif maze_drop_down.get_first() == 'Maze 3':
            # Reassign variables with respect to the new maze
            display, surf, graph1, maze_img, \
                centered_w, centered_h, start, end, once = initialize_maze('mazes/maze3.png')
            alg.update_off_set_values(centered_w, centered_h)
            draw_text_box = False
        elif maze_drop_down.get_first() == 'Other':
            # If other is selected, allow the text box to be drawn
            draw_text_box = True

    # If the textbox is active, update it
    if draw_text_box:
        # Update and get the returned text
        returned_text = maze_drop_down_text_box.update(events)
        if returned_text is not None:
            try:
                # If there is a valid input, switch to that maze.

                # If the maze is circular, do not run the crop.
                print(returned_text)
                if returned_text[6] == 'c':
                    print('true')
                    display, surf, graph1, maze_img, \
                        centered_w, centered_h, start, end, once = initialize_maze(returned_text,
                                                                               False)
                else:
                    display, surf, graph1, maze_img, \
                        centered_w, centered_h, start, end, once = initialize_maze(returned_text)
                alg.update_off_set_values(centered_w, centered_h)
            except Exception:  # Exception is broad here because Cv2 does not give good error
                print('Path does not exist')  # messages, however the error is caused by the path
                # location not close enough

    # Pygame
    display.blit(surf, (0, 0))
    pygame.time.wait(1)
    pygame.display.flip()

# cv2.imshow('w', thinned)
#
# cv2.waitKey(0)
