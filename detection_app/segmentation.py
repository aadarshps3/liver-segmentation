import numpy as np
import cv2 as cv


import cv2 as cv

import matplotlib.pyplot as plt


img=0
curimg=0
def segment(image):
  # image=cv.imread(image)
  img=np.array(image)
  curimg=np.array(img)
  gray = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)
  ret,thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
  kernel = np.ones((3, 3), np.uint8)
  opening = cv.morphologyEx(thresh, cv.MORPH_OPEN,kernel, iterations=2)
  curimg = opening
  sure_bg = cv.dilate(curimg, kernel, iterations=3)
  dist_transform = cv.distanceTransform(curimg, cv.DIST_L2, 5)
  ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
  sure_fg = np.uint8(sure_fg)
  unknown = cv.subtract(sure_bg, sure_fg)
  ret, markers = cv.connectedComponents(sure_fg)
  markers = markers + 1
  # Now mark the region of unknown with zero
  markers[unknown == 255] = 0
  markers = cv.watershed(img, markers)
  img[markers == -1] = [255, 0, 0]

  tumorImage = cv.cvtColor(img, cv.COLOR_HSV2BGR)
  curimg = tumorImage
  return curimg









