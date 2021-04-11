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
