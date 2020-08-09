import cv2
import pyautogui
import numpy as np

im1 = pyautogui.screenshot()
open_cv_image = np.array(im1)
open_cv_image = open_cv_image[:, :, ::-1].copy()

cv2.imshow('test', open_cv_image)
cv2.waitKey()