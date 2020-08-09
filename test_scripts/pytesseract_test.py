import cv2
import math
import numpy as np
from imutils import contours
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Load image with characteristics
image = cv2.imread('../data/test_sudoku_2.jpg')
image_height, image_width, image_channels = image.shape
block_size = int(image_width / 9) | 1
block_min_area = int(image_width / 20 * image_width / 20)
block_max_area = int(image_width / 9 * image_width / 9)

# Gray-scale and threshold the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, int(block_size), 5)
invert_orig = 255 - thresh

# Display the image
cv2.imshow('temp', thresh)
cv2.waitKey()

# Find the contours
contourss = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contourss = contourss[0] if len(contourss) == 2 else contourss[1]
for block in contourss:
    area = cv2.contourArea(block)
    if area < block_min_area:
        cv2.drawContours(thresh, [block], -1, (0, 0, 0), -1)

# Display the image
cv2.imshow('temp', thresh)
cv2.waitKey()

# Fix horizontal and vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

# Display the image
cv2.imshow('temp', thresh)
cv2.waitKey()

# Sort by top to bottom and each row by left to right
invert = 255 - thresh
cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

good_contours = []
for i, c in enumerate(cnts, 1):
    contour_area = cv2.contourArea(c)
    if block_min_area < contour_area < block_max_area:
        good_contours.append(c)
dimension = int(math.sqrt(len(good_contours)))

(cnts, _) = contours.sort_contours(good_contours, method="top-to-bottom")

board = []
row = []
for i, c in enumerate(cnts, 1):
    row.append(c)
    if i % dimension == 0:
        (cntsz, _) = contours.sort_contours(row, method="left-to-right")
        board.append(cntsz)
        row = []

mask = np.zeros(image.shape, dtype=np.uint8)

# Iterate through each box
for row in board:
    for c in row:
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = invert_orig[y + 5:y + h - 10, x + 5:x + w - 10]
        if np.average(cropped_image) > 253:
            print(" ", end=" ")
        else:
            print(pytesseract.image_to_string(cropped_image, config='--psm 10'), end=" ")
        cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
    print()

result = cv2.bitwise_and(image, mask)
result[mask == 0] = 255
cv2.imshow('result', result)
cv2.waitKey()
