import numba
import numpy as np
import math
from typing import Tuple

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

    @staticmethod
    def euclidean_distance(node1, node2):
        """Computes the euclidean distance between two points using Pythagoreas' theorem."""

        return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

    def closest_path(self, point, radius):
        temp = []

        for y in range(point[1] - radius - 1, point[1] + radius):
            for x in range(point[0] - radius - 1, point[0] + radius):

                if 0 <= y < self.rows and 0 <= x < self.cols and self.graph[x, y] == 1:
                    temp.append((x, y))
        index = 0
        min_so_far = self.euclidean_distance(temp[0], point)

        for i in range(len(temp)):
            if self.euclidean_distance(temp[i], point) < min_so_far:
                min_so_far = self.euclidean_distance(temp[i], point)
                index = i

        return temp[index]
