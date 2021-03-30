import cv2
import numpy as np
from typing import Tuple
import numba
import pygame
import math

pygame.init()

maze = 'maze2.jpg'

image = cv2.resize(cv2.imread(maze), (1280, 720))

retVal, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)

thinned = np.array(cv2.ximgproc.thinning(thresh)) // 255

# cut borders

temp = np.delete(thinned, [0, thinned.shape[1] - 1], axis=1)
temp = np.delete(thinned, [0, thinned.shape[0] - 1], axis=0)

# This along with the decorator complies each method into machine code the first
# time its called. Then each subsequent call runs from machine code meaning
# any method that is used a lot (like get_valid_neighbours) or has a lot of
# loops will benefit from numba.


# You can try timing 10,000,000 calls to get_valid_neighbours with numba and
# without (comment out decorator).

# Note: the first call to a method may be slower
spec = [
    ('graph', numba.uint8[:, :]),
    ('rows', numba.uint16),
    ('cols', numba.uint16)
]


@numba.experimental.jitclass(spec)
class MatrixGraph(object):
    """This class will take care of all graph operations. Each node is a pixel of
    the graph with a value of either 0 or 1. Edges are implicitly stored as the
    8 nodes (pixels) around each node.

    Note: This is a jitclass so type of inputs is very sensitive.
    """

    graph: np.ndarray
    rows: int
    cols: int

    def __init__(self, matrix: np.ndarray) -> None:
        self.graph = matrix
        self.cols, self.rows = matrix.shape

    def get_valid_neighbours(self, col, row) -> list[Tuple]:
        """Not elegant but fast(enough for now)"""
        neighbours = []
        # col = cord[0]
        # row = cord[1]

        if row - 1 >= 0 and self.graph[col, row - 1] == 1:
            neighbours.append((col, row - 1))
        if row + 1 < self.rows and self.graph[col, row + 1] == 1:
            neighbours.append((col, row + 1))
        if col - 1 >= 0 and self.graph[col - 1, row] == 1:
            neighbours.append((col - 1, row))
        if col + 1 < self.cols and self.graph[col + 1, row] == 1:
            neighbours.append((col + 1, row))
        if row - 1 >= 0 and col - 1 >= 0 and self.graph[col - 1, row - 1] == 1:
            neighbours.append((col - 1, row - 1))
        if row - 1 >= 0 and col + 1 < self.cols and self.graph[col + 1, row - 1] == 1:
            neighbours.append((col + 1, row - 1))
        if row + 1 < self.rows and col - 1 >= 0 and self.graph[col - 1, row + 1] == 1:
            neighbours.append((col - 1, row + 1))
        if row + 1 < self.rows and col + 1 < self.cols and self.graph[col + 1, row + 1] == 1:
            neighbours.append((col + 1, row + 1))
        return neighbours

    def euclidean_distance(self, node1, node2):
        """Computes the euclidean distance between two points using Pythagoreas' theorem."""

        return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)


class PathfindingAlgorithms:

    def depth_first_search(self, graph: MatrixGraph, curr: Tuple[int, int], target: Tuple[int, int],
                           visited, surface):
        if curr == target:
            return True

        surface.set_at(curr, (255, 0, 0))
        display.blit(surf, (0, 0))
        pygame.display.flip()

        print(curr)

        visited.append(curr)
        for node in graph.get_valid_neighbours(curr[0], curr[1]):
            if node not in visited:
                self.depth_first_search(graph, node, target, visited, surface)
        return False

    def breadth_first_search(self, graph, start, target, visited: set, surface):
        queue = []
        queue.extend(graph.get_valid_neighbours(start[0], start[1]))
        visited.update(graph.get_valid_neighbours(start[0], start[1]))

        while queue != []:

            curr = queue.pop(0)

            # surface.set_at(curr, (255, 0, 0))

            pygame.draw.circle(surface, (255, 0, 0), curr, 3)
            display.blit(surf, (0, 0))
            pygame.display.flip()

            if curr == target:
                return True
            for node in graph.get_valid_neighbours(curr[0], curr[1]):
                if node not in visited:
                    queue.append(node)
                    visited.add(node)
        return False

    def depth_first_search_iterative(self, graph: MatrixGraph, start: Tuple, target: Tuple, surface) -> bool:
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

            pygame.draw.circle(surface, (255, 0, 0), vertex, 3)
            display.blit(surf, (0, 0))
            pygame.display.flip()

            if vertex == target:
                return True
            elif vertex not in discovered:
                discovered.add(vertex)
                neighbors = graph.get_valid_neighbours(vertex[0], vertex[1])
                for neighbor in neighbors:
                    stack.append(neighbor)
        return False


graph1 = MatrixGraph(np.swapaxes(temp, 0, 1))

# cv2.imshow('t', temp * 255)
# cv2.waitKey(0)

pygame.init()
display = pygame.display.set_mode((1280, 720))
maze_img = pygame.transform.scale(pygame.image.load(maze), (1280, 720))
display.blit(maze_img, (0, 0))

# surf = pygame.surfarray.make_surface(graph1.graph * 255)
surf = pygame.Surface((1280, 720), pygame.SRCALPHA, 32)
surf = surf.convert_alpha()

display.blit(surf, (0, 0))
alg = PathfindingAlgorithms()
# alg.breadth_first_search(graph1, (1212, 709), (393, 432), set(), surf)
alg.depth_first_search_iterative(graph1, (1212, 709), (393, 432), surf)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                posx, posy = pygame.mouse.get_pos()
                print((posx, posy), graph1.graph[posx][posy])
            except:
                pass

    pygame.time.wait(1)
    pygame.display.flip()


# cv2.imshow('w', thinned)
#
# cv2.waitKey(0)
