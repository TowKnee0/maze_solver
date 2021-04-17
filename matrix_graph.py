"""
matrix_graph.py:
Contains the MatrixGraph class which is used to store pixel connections

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""

import math
import numba
import numpy as np

# Numba requirements
spec = [
    ('graph', numba.uint8[:, :]),
    ('rows', numba.uint16),
    ('cols', numba.uint16)
]


@numba.experimental.jitclass(spec)
class MatrixGraph:
    """This class will take care of all graph operations. Each node is a pixel of
    the graph with a value of either 0 or 1. Edges are implicitly stored as the
    8 nodes (pixels) around each node.

    Note: This is a jitclass so type of inputs is very sensitive.
    """

    graph: np.ndarray
    rows: int
    cols: int

    def __init__(self, matrix: np.ndarray) -> None:
        """
        Initialize a Matrix Graph
        """
        self.graph = matrix
        self.cols, self.rows = matrix.shape

    def get_valid_neighbours(self, col: int, row: int) -> list[tuple]:
        """
        Return a list of pixels that are adjacent to (col, row)
        """
        neighbours = []

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
    def euclidean_distance(node1: tuple[int, int], node2: tuple[int, int]) -> float:
        """
        Return a float that represents the euclidean distance between two points using Pythagoreas'
        Theorem
        """

        return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

    def closest_path(self, point: tuple[int, int], radius: int) -> tuple[int, int]:
        """
        Return a tuple of ints that represents the closest path to point within a certain radius
        """
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


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['numba', 'numpy', 'math'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
