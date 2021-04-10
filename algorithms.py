"""
algorithms.py:
Contains the PathfindingAlgorithms class which contains various path finding functions.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import pygame
from matrix_graph import MatrixGraph
from typing import Tuple


class PathfindingAlgorithms:
    """
    A class used to store various path finding pathfinding algorithms

    Sample Usage:
    >>> algorithms = PathfindingAlgorithms()
    """

    def breadth_first_search(self, graph: MatrixGraph, start: tuple, target: tuple, visited: set,
                             surface, display) -> bool:
        """
        Return true if target is found, return false otherwise.

        This function is an implementation of the breadth_first_search pathfinding algorithm
        """
        queue = []
        queue.extend(graph.get_valid_neighbours(start[0], start[1]))
        visited.update(graph.get_valid_neighbours(start[0], start[1]))

        while queue != []:

            curr = queue.pop(0)

            # Visualize step
            pygame.draw.circle(surface, (255, 0, 0), curr, 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if curr == target:
                return True
            for node in graph.get_valid_neighbours(curr[0], curr[1]):
                if node not in visited:
                    queue.append(node)
                    visited.add(node)
        return False

    def depth_first_search_iterative(self, graph: MatrixGraph, start: tuple, target: tuple,
                                     surface, display) -> bool:
        """
        Return true if target is found, return false otherwise.

        This is an iterative version of depth_first_search, since the recursive version exceeds
        the maximum recursion depth.
        """
        discovered = set()
        stack = [start]  # Stack is a reversed list for now. Later we can make a stack class if we
        # need

        while stack != []:
            vertex = stack.pop()

            # Visualize step
            pygame.draw.circle(surface, (255, 0, 0), vertex, 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if vertex == target:
                return True
            elif vertex not in discovered:
                discovered.add(vertex)
                neighbors = graph.get_valid_neighbours(vertex[0], vertex[1])
                for neighbor in neighbors:
                    stack.append(neighbor)
        return False
