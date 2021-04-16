"""
algorithms.py:
Contains the PathfindingAlgorithms class which contains various path finding functions.

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

from queue import PriorityQueue
import pygame
from matrix_graph import MatrixGraph
from clock import Timer


class PathfindingAlgorithms:
    """
    A class used to store various path finding pathfinding algorithms

    Private Instance Attributes:
        - _iteration_text_background: A white pygame surface that acts as a background for the
                                     text of the iteration counter
        - _iteration_text_pos: A tuple that represents where to draw the iteration counter
        - _timer_text_background: A white pygame surface that acts as a background for the
                                  text of the timer
        - _timer_text_pos: A tuple that represents where to draw the timer
        - _maze_x_offset: An integer that represents how much the drawing of the maze needs to be
                         shifted in the x direction inorder to account for the maze being centered
        - _maze_y_offset: An integer that represents how much the drawing of the maze needs to be
                         shifted in the y direction inorder to account for the maze being centered
    Sample Usage:
    >>> algorithms = PathfindingAlgorithms((200, 200), 5, 5, (500, 500))
    """

    _iteration_text_background: pygame.Surface
    _iteration_text_pos: tuple[int, int]
    _timer_text_background: pygame.Surface
    _timer_text_pos: tuple[int, int]
    _maze_x_offset: int
    _maze_y_offset: int

    def __init__(self, iteration_counter_pos: tuple[int, int], maze_x_offset: int,
                 maze_y_offset: int, timer_text_pos: tuple[int, int]) -> None:
        """
        Initialize a PathfindingAlgorithms Object
        """
        # Max variables are used to generate the largest background
        max_string = f'Nodes Searched + {1920 * 1080}'
        max_time = 'Timer: 99:99:99'

        # Assign instance attributes
        self._iteration_text_background = _get_text_surface(max_string)
        self._iteration_text_pos = iteration_counter_pos
        self._timer_text_pos = timer_text_pos
        self._timer_text_background = _get_text_surface(max_time)
        self._maze_x_offset = maze_x_offset
        self._maze_y_offset = maze_y_offset

    def breadth_first_search(self, graph: MatrixGraph, start: tuple, target: tuple,
                             surface: pygame.Surface, display: pygame.Surface) \
            -> list[tuple[int, int]]:
        """
        Return a list of tuples representing the final path if target is found,
        return an empty list otherwise.

        This function is an implementation of the breadth_first_search pathfinding algorithm
        """
        queue = []
        visited = set()
        paths = {}  # A dictionary that maps new nodes to the previous node
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
            iteration_counter = f'Nodes Searched: {counter}'
            self._draw_loop_iterations(iteration_counter, surface)

            # Pop the current node
            curr = queue.pop(0)

            # Visualize step
            _ = pygame.event.get()  # Call event.get to stop program from crashing on clicks
            curr_x = curr[0] + self._maze_x_offset + 1
            curr_y = curr[1] + self._maze_y_offset + 1
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
                                     surface: pygame.Surface, display: pygame.Surface) \
            -> list[tuple[int, int]]:
        """
        Return a list of tuples representing the final path if target is found,
        return an empty list otherwise.

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
            iteration_counter = f'Nodes Searched: {counter}'
            self._draw_loop_iterations(iteration_counter, surface)

            vertex = stack.pop()

            # Visualize step
            _ = pygame.event.get()  # Call event.get to stop program from crashing on clicks
            curr_x = vertex[0] + self._maze_x_offset + 1
            curr_y = vertex[1] + self._maze_y_offset + 1
            pygame.draw.circle(surface, (255, 0, 0), (curr_x, curr_y), 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if vertex == target:
                found = True
            elif vertex not in discovered:
                discovered.add(vertex)
                neighbors = graph.get_valid_neighbours(vertex[0], vertex[1])
                for neighbor in neighbors:
                    if neighbor not in discovered:
                        # Add the neighbor as a key in the path dictionary with vertex as a parent
                        stack.append(neighbor)
                        paths[neighbor] = vertex

            clock.update_time()
            self._draw_timer(clock, surface)

        if found is False:
            return []
        else:
            return self._find_and_draw_final_path(paths, start, target, surface, display)

    def a_star(self, graph: MatrixGraph, start: tuple, target: tuple,
               surface: pygame.Surface, display: pygame.Surface) -> list[tuple[int, int]]:
        """
        The heuristic used is the distance from target to the current node
        if f(n) = 0 we have reached our node, our promising choice is the min(f(n)) for each
        neighbour
        """

        open_queue = PriorityQueue()
        open_queue.put((graph.euclidean_distance(start, target), (start, 0)))

        closed = {start}

        paths = {}  # A dictionary that maps new nodes to the previous node
        found = False
        # Variables and Surfaces used to display the current iterations
        counter = 0

        # Pygame clock
        clock = Timer()

        while not open_queue.empty() and not found:
            # Draw and update iteration counter
            counter += 1
            iteration_counter = f'Nodes Searched: {counter}'
            self._draw_loop_iterations(iteration_counter, surface)

            curr = open_queue.get()
            closed.add(curr[1][0])

            _ = pygame.event.get()  # Call event.get to stop program from crashing on clicks
            curr_x = curr[1][0][0] + self._maze_x_offset + 1
            curr_y = curr[1][0][1] + self._maze_y_offset + 1
            pygame.draw.circle(surface, (255, 0, 0), (curr_x, curr_y), 3)
            display.blit(surface, (0, 0))
            pygame.display.flip()

            if curr[1][0] == target:
                found = True

            neighbours = graph.get_valid_neighbours(curr[1][0][0], curr[1][0][1])

            for coord in neighbours:
                if coord in closed:
                    # If the neighbor has already been computed, do nothing
                    continue
                if not any(tup[1][0] == coord for tup in open_queue.queue):
                    # If the neighbor is not in the the open queue, add it

                    # Compute the huristic and add it to open
                    neighbour_f = curr[1][1] + 1 + graph.euclidean_distance(target, coord)
                    open_queue.put((neighbour_f, (coord, curr[1][1] + 1)))

                    # Track the path
                    paths[coord] = curr[1][0]

            # Update clock
            clock.update_time()
            self._draw_timer(clock, surface)

        if found is False:
            return []
        else:
            return self._find_and_draw_final_path(paths, start, target, surface, display)

    def update_off_set_values(self, centered_w: int, centered_h: int) -> None:
        """
        Update the off set attributes. This method is called when the program swaps mazes.
        """
        self._maze_x_offset = centered_w
        self._maze_y_offset = centered_h

    def _find_and_draw_final_path(self, paths: dict[tuple[int, int], tuple[int, int]],
                                  start: tuple, target: tuple, surface: pygame.Surface,
                                  display: pygame.Surface) -> list[tuple[int, int]]:
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
            curr_x = current_node[0] + self._maze_x_offset + 1
            curr_y = current_node[1] + self._maze_y_offset + 1
            pygame.draw.circle(surface, (0, 255, 0), (curr_x, curr_y), 3)

        # Insert the first node
        final_path_so_far.insert(0, start)

        # Draw the final path
        pygame.draw.circle(surface, (0, 255, 0), (start[0] + self._maze_x_offset + 1,
                                                  start[1] + self._maze_y_offset + 1), 3)
        display.blit(surface, (0, 0))
        pygame.display.flip()
        return final_path_so_far

    def _draw_loop_iterations(self, loop_iters: str, surface: pygame.Surface) -> None:
        """
        Draw the current loop iterations at the specified position
        """
        text_surface = pygame.font.SysFont('Arial', 20).render(loop_iters, True, (0, 0, 0))
        surface.blit(self._iteration_text_background, self._iteration_text_pos)
        surface.blit(text_surface, self._iteration_text_pos)

    def _draw_timer(self, clock: Timer, surface: pygame.Surface) -> None:
        text_surface = clock.get_text_surface()
        surface.blit(self._timer_text_background, self._timer_text_pos)
        surface.blit(text_surface, self._timer_text_pos)


def _get_text_surface(longest_text: str) -> pygame.Surface:
    """
    Return a white box that is the size of the maximum possible text being rendered
    """
    text_surface = pygame.font.SysFont('Arial', 20).render(longest_text, True, (0, 0, 0))
    text_h = text_surface.get_height()
    text_w = text_surface.get_width()
    white = pygame.Surface((text_w, text_h))
    white.fill((255, 255, 255))
    return white


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['pygame', 'matrix_graph', 'typing', 'clock', 'queue'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
