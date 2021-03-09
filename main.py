import cv2
import skan
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
import numba

image = cv2.imread('maze2.jpg')

retVal, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

thinned = np.array(cv2.ximgproc.thinning(thresh))//255


# This along with the decorator complies each method into machine code the first
# time its called. Then each subsequent call runs from machine code meaning
# any method that is used a lot (like get_valid_neighbours) or has a lot of
# loops will benefit from numba.


# You can try timing 10,000,000 calls to get_valid_neighbours with numba and
# without (comment out decorator).

# Note: the first call to a method may be slower
spec = [
        ('graph', numba.uint8[:, :]),
        ('rows', numba.uint8),
        ('cols', numba.uint8)
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
        self.rows, self.cols = matrix.shape

    def get_valid_neighbours(self, row: int, col: int) -> list[Tuple]:
        """Not elegant but fast(enough for now)"""
        neighbours = []

        if row - 1 >= 0 and self.graph[row - 1, col] == 1:
            neighbours.append((row - 1, col))
        if row + 1 < self.rows and self.graph[row + 1, col] == 1:
            neighbours.append((row + 1, col))
        if col - 1 >= 0 and self.graph[row, col - 1] == 1:
            neighbours.append((row, col - 1))
        if col + 1 < self.cols and self.graph[row, col + 1] == 1:
            neighbours.append((row, col + 1))
        if row - 1 >= 0 and col - 1 >= 0 and self.graph[row - 1, col - 1] == 1:
            neighbours.append((row - 1, col - 1))
        if row - 1 >= 0 and col + 1 < self.cols and self.graph[row - 1, col + 1] == 1:
            neighbours.append((row - 1, col + 1))
        if row + 1 < self.rows and col - 1 >= 0 and self.graph[row + 1, col - 1] == 1:
            neighbours.append((row + 1, col - 1))
        if row + 1 < self.rows and col + 1 < self.cols and self.graph[row + 1, col + 1] == 1:
            neighbours.append((row + 1, col + 1))
        return neighbours


class PathfindingAlgorithms:

    def depth_first_search(self, graph: MatrixGraph, curr: Tuple[int, int], target: Tuple[int, int], visited):
        if curr == target:
            return True

        visited.append(curr)
        for node in graph.get_valid_neighbours(curr[0], curr[1]):
            if node not in visited:
                self.depth_first_search(graph, node, target, visited)
        return False


graph1 = MatrixGraph(thinned)

# cv2.imshow('w', thinned)
#
# cv2.waitKey(0)
