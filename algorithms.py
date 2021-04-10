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
                             surface, display) -> list[tuple]:
        """
        Return true if target is found, return false otherwise.

        This function is an implementation of the breadth_first_search pathfinding algorithm
        """
        queue = []
        paths = {}
        queue.extend(graph.get_valid_neighbours(start[0], start[1]))
        visited.update(graph.get_valid_neighbours(start[0], start[1]))

        # Update paths with the original visited set
        for node in graph.get_valid_neighbours(start[0], start[1]):
            paths[node] = start
        found = False

        while queue != [] and not found:

            curr = queue.pop(0)

            # Visualize step
            pygame.draw.circle(surface, (255, 0, 0), curr, 3)
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


        if found is False:
            return []
        else:
            # Trace the path back to the start, the list is traversed backwards, so we insert to
            # the front of the list
            final_path = []
            current_node = target
            while current_node != start:
                final_path.insert(0, current_node)
                current_node = paths[current_node]
                # Draw the final path
                pygame.draw.circle(surface, (0, 255, 0), current_node, 3)

            # Insert the first node
            final_path.insert(0, start)

            # Draw the final path
            pygame.draw.circle(surface, (0, 255, 0), start, 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()
            return final_path

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

        while stack != [] and not found:
            vertex = stack.pop()

            # Visualize step
            pygame.draw.circle(surface, (255, 0, 0), vertex, 3)
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

        if found is False:
            return []
        else:
            # Trace the path back to the start, the list is traversed backwards, so we insert to
            # the front of the list
            final_path = []
            current_node = target
            while current_node != start:
                final_path.insert(0, current_node)
                current_node = paths[current_node]
                # Draw the final path
                pygame.draw.circle(surface, (0, 255, 0), current_node, 3)

            # Insert the first node
            final_path.insert(0, start)

            # Draw the final path
            pygame.draw.circle(surface, (0, 255, 0), start, 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()
            return final_path

