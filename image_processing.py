"""
image_processing.py:
Contains a method used to handle processing the input images

CSC111 Final Project by Tony He, Austin Blackman, Ifaz Alam
"""
import cv2
import numpy as np


def crop_image(image: np.ndarray) -> np.ndarray:
    """
    Return a cropped version of the inputted maze image.

    This function is used to find the two longest contours (edges) and trims the unnecessary parts
    of the image
    """
    # convert image to grayscale and apply blur to reduce noise
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(image_gray, (3, 3), 0)

    # global threshold using Otsu
    # Note: Although unpacking like this results in one of the variables to be unused and makes
    # PyTA heavily depressed, this is standard OpenCV notation.
    # For reference, you may check docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html

    ret1, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # invert image color and find contours
    ret2, thresh2 = cv2.threshold(thresh1, 150, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # create list of tuples with the contour itself and its arc length
    # then sort by arc length and take the two longest
    cont_len = [(cont, cv2.arcLength(cont, True)) for cont in contours]
    cont_len.sort(key=lambda x: -x[1])
    longest_2 = cont_len[0:2]
    rects = [cv2.boundingRect(tup[0]) for tup in longest_2]

    # take the smallest coordinates for the top left corner of rect
    # and largest for the bottom right corner
    min_x0, min_y0, max_x0, max_y0 = rects[0][0], rects[0][1], \
                                     rects[0][0] + rects[0][2], \
                                     rects[0][1] + rects[0][3]
    min_x1, min_y1, max_x1, max_y1 = rects[1][0], rects[1][1], \
                                     rects[1][0] + rects[1][2], \
                                     rects[1][1] + rects[1][3]
    min_x = min(min_x0, min_x1) + 1
    min_y = min(min_y0, min_y1) + 1
    max_x = max(max_x0, max_x1) - 1
    max_y = max(max_y0, max_y1) - 1

    cropped_img = image[min_y: max_y, min_x: max_x]
    return cropped_img


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['cv2', 'numpy'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
