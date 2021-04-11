import cv2

def crop_image(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(image_gray, (3, 3), 0)

    ret1, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ret2, thresh2 = cv2.threshold(thresh1, 150, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cont_per = [(cont, cv2.arcLength(cont, True)) for cont in contours]
    cont_per.sort(key=lambda x: -x[1])
    longest_2 = cont_per[0:2]
    rects = [cv2.boundingRect(tup[0]) for tup in longest_2]

    min_x0, min_y0, max_x0, max_y0 = rects[0][0], rects[0][1], rects[0][0] + rects[0][2], rects[0][1] + rects[0][3]
    min_x1, min_y1, max_x1, max_y1 = rects[1][0], rects[1][1], rects[1][0] + rects[1][2], rects[1][1] + rects[1][3]
    min_x = min(min_x0, min_x1)
    min_y = min(min_y0, min_y1)
    max_x = max(max_x0, max_x1)
    max_y = max(max_y0, max_y1)

    filtered_copy = thresh1.copy()
    cv2.rectangle(filtered_copy, (min_x, min_y), (max_x, max_y), 0, 1)

    cropped_img = image[min_y: max_y, min_x: max_x]
    return cropped_img
