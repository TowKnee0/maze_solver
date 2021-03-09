import cv2
import skan
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
import numba

image = cv2.imread('maze.png')

retVal, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

thinned = np.array(cv2.ximgproc.thinning(thresh))//255



class MatrixGraph:

    graph: np.ndarray
    rows: int
    cols: int

    def __init__(self, matrix: np.ndarray) -> None:
        self.graph = matrix
        self.rows, self.cols = matrix.shape

    # @numba.jit(nopython=True) use if performance is an issue. requires restructure
    def get_valid_neighbours(self, row: int, col: int) -> list[Tuple]:
        """Not elegant but fast"""
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


graph = MatrixGraph(thinned)
