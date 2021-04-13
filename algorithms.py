"""
algorithms.py:
Contains the PathfindingAlgorithms class which contains various path finding functions.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import pygame
from matrix_graph import MatrixGraph
from typing import Tuple
from clock import Timer


class PathfindingAlgorithms:
    """
    A class used to store various path finding pathfinding algorithms

    Instance Attributes:
        - iteration_text_background: A white pygame surface that acts as a background for the
                                     text of the iteration counter
        - iteration_text_pos: A tuple that represents where to draw the iteration counter
        - maze_x_offset: An integer that represents how much the drawing of the maze needs to be
                         shifted in the x direction inorder to account for the maze being centered
        - maze_y_offset: An integer that represents how much the drawing of the maze needs to be
                         shifted in the y direction inorder to account for the maze being centered
    Sample Usage:
    >>> algorithms = PathfindingAlgorithms((200, 200))
    """

    iteration_text_background: pygame.Surface
    iteration_text_pos: tuple[int, int]
    timer_text_pos: tuple[int, int]
    timer_text_background: pygame.Surface
    maze_x_offset: int
    maze_y_offset: int

    def __init__(self, iteration_counter_pos: tuple[int, int], maze_x_offset: int,
                 maze_y_offset: int, timer_text_pos: tuple[int, int]) -> None:
        """
        Initialize a PathfindingAlgorithms Object
        """
        max_string = f'Current Iteration + {1920 * 1080}'  # Max is the largest number of pixels
        max_time = f'TIMER: 99:99:99'
        # possible to search
        self.iteration_text_background = self._get_text_surface(max_string)
        self.iteration_text_pos = iteration_counter_pos
        self.timer_text_pos = timer_text_pos
        self.timer_text_background = self._get_text_surface(max_time)
        self.maze_x_offset = maze_x_offset
        self.maze_y_offset = maze_y_offset

    def breadth_first_search(self, graph: MatrixGraph, start: tuple, target: tuple,
                             surface, display) -> list[tuple]:
        """
        Return true if target is found, return false otherwise.

        This function is an implementation of the breadth_first_search pathfinding algorithm
        """
        queue = []
        visited = set()
        paths = {}
        queue.extend(graph.get_valid_neighbours(start[0], start[1]))
        visited.update(graph.get_valid_neighbours(start[0], start[1]))

        # Update paths with the original visited set
        for node in graph.get_valid_neighbours(start[0], start[1]):
            paths[node] = start
        found = False

        # Counter to store current iteration
        counter = 0

        # Pygame clock
        clock = Timer()

        while queue != [] and not found:
            # Draw and update the loop iteration counter
            counter += 1
            iteration_counter = f'Current Iteration: {counter}'
            self._draw_loop_iterations(iteration_counter, surface)

            # Pop the current node
            curr = queue.pop(0)

            # Visualize step
            curr_x = curr[0] + self.maze_x_offset
            curr_y = curr[1] + self.maze_y_offset
            pygame.draw.circle(surface, (255, 0, 0), (curr_x, curr_y), 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if curr == target:
                found = True
            for node in graph.get_valid_neighbours(curr[0], curr[1]):
                if node not in visited:
                    queue.append(node)
                    visited.add(node)

                    # Add the node as a key with the current node as the value
                    paths[node] = curr

            clock.update_time()
            self._draw_timer(clock, surface)

        if found is False:
            return []
        else:
            return self._find_and_draw_final_path(paths, start, target, surface, display)

    def depth_first_search_iterative(self, graph: MatrixGraph, start: tuple, target: tuple,
                                     surface, display) -> list[tuple[int, int]]:
        """
        Return true if target is found, return false otherwise.

        This is an iterative version of depth_first_search, since the recursive version exceeds
        the maximum recursion depth.
        """
        discovered = set()
        stack = [start]  # Stack is a reversed list for now. Later we can make a stack class if we
        # need
        paths = {}  # A dictionary that maps new nodes to the previous node
        found = False

        # Variables and Surfaces used to display the current iterations
        counter = 0

        # Pygame clock
        clock = Timer()

        while stack != [] and not found:
            # Draw and update the loop iteration counter
            counter += 1
            iteration_counter = f'Current Iteration: {counter}'
            self._draw_loop_iterations(iteration_counter, surface)

            vertex = stack.pop()

            # Visualize step
            curr_x = vertex[0] + self.maze_x_offset
            curr_y = vertex[1] + self.maze_y_offset
            pygame.draw.circle(surface, (255, 0, 0), (curr_x, curr_y), 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if vertex == target:
                found = True
            elif vertex not in discovered:
                discovered.add(vertex)
                neighbors = graph.get_valid_neighbours(vertex[0], vertex[1])
                for neighbor in neighbors:
                    stack.append(neighbor)
                    if neighbor not in discovered:
                        # Add the neighbor as a key in the path dictionary with vertex as a parent
                        paths[neighbor] = vertex

            clock.update_time()
            self._draw_timer(clock, surface)

        if found is False:
            return []
        else:
            return self._find_and_draw_final_path(paths, start, target, surface, display)

    def a_star(self, graph: MatrixGraph, start: tuple, target: tuple,
               surface, display) -> list[tuple]:
        """
        The heuristic used is the distance from target to the current node
        if f(n) = 0 we have reached our node, our promising choice is the min(f(n)) for each
        neighbour
        """
        # Priority queue of tuples (node, step cost, distance from target, prev_node)
        # priority with respect to smallest distance from target
        # (start, 0, graph.euclidean_distance(start, target), None)

        priority_queue = [[start, 0, graph.euclidean_distance(start, target), None]]
        found = False
        prev = None
        curr = start
        step = 0

        path = []

        # visited.update(graph.get_valid_neighbours(start[0], start[1]))

        while found is not True:
            for node in graph.get_valid_neighbours(curr[0], curr[1]):
                if node != prev:
                    # the cost to go from the current node to the next node
                    step_cost = step + graph.euclidean_distance(curr, node)

                    # distance from the next node to the target
                    heuristic = graph.euclidean_distance(node, target)

                    if heuristic == 0:
                        found = True

                    # the combined cost
                    total_cost = step_cost + heuristic

                    # the node that was traversed to reach this node
                    prev = curr

                    # update existing values that are checked
                    if node in {x[0] for x in priority_queue}:
                        for item in priority_queue:
                            if node == item[0]:
                                item[1] = step_cost
                                item[2] = total_cost
                                item[3] = prev

                    else:
                        priority_queue.append([node, step_cost, total_cost, prev])
                print(priority_queue)
                # sort the priority queue
                if priority_queue != []:
                    while not (priority_queue[-1][2] <= priority_queue[-2][2]):
                        priority_queue[-1][2], priority_queue[-2][2] = priority_queue[-2][2], \
                                                                       priority_queue[-1][2]

            # Visualize step
            pygame.draw.circle(surface, (255, 0, 0), priority_queue[-1][0], 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            # our new node is the prioritized one
            curr = priority_queue[-1][0]
            step = priority_queue[-1][1]

            node_info = priority_queue.pop()[0]
            col, row = node_info[0], node_info[1]
            path.append((col, row))

        return path

    def _find_and_draw_final_path(self, paths: dict[tuple[int, int], tuple[int, int]],
                                  start: tuple, target: tuple, surface, display) -> \
            list[tuple[int, int]]:
        """
        Return a list of tuples that corresponds to the path found by the algorithm that calls
        this function
        """

        final_path_so_far = []
        current_node = target
        while current_node != start:
            final_path_so_far.insert(0, current_node)
            current_node = paths[current_node]
            # Draw the final path
            curr_x = current_node[0] + self.maze_x_offset
            curr_y = current_node[1] + self.maze_y_offset
            pygame.draw.circle(surface, (0, 255, 0), (curr_x, curr_y), 3)

        # Insert the first node
        final_path_so_far.insert(0, start)

        # Draw the final path
        pygame.draw.circle(surface, (0, 255, 0), (start[0] + self.maze_x_offset,
                                                  start[0] + self.maze_y_offset), 3)
        display.blit(surface, (0, 0))
        pygame.display.flip()
        return final_path_so_far

    def _draw_loop_iterations(self, loop_iters: str, surface: pygame.Surface) -> None:
        """
        Draw the current loop iterations at the specified position
        """
        text_surface = pygame.font.SysFont('Arial', 20).render(loop_iters, True, (0, 0, 0))
        surface.blit(self.iteration_text_background, self.iteration_text_pos)
        surface.blit(text_surface, self.iteration_text_pos)

    def _draw_timer(self, clock: Timer, surface: pygame.Surface) -> None:
        text_surface = clock.get_text_surface()
        surface.blit(self.timer_text_background, self.timer_text_pos)
        surface.blit(text_surface, self.timer_text_pos)

    def _get_text_surface(self, longest_text: str) -> pygame.Surface:
        """
        Return a white box that is the size of the maximum possible text being rendered
        """
        text_surface = pygame.font.SysFont('Arial', 20).render(longest_text, True, (0, 0, 0))
        text_h = text_surface.get_height()
        text_w = text_surface.get_width()
        white = pygame.Surface((text_w, text_h))
        white.fill((255, 255, 255))
        return white

