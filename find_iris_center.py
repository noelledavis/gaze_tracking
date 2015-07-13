# find_iris_center.py
# Find iris center from eye image.

from __future__ import division
import cv2
import numpy as np

# resize image
def resize(img, new_width = 500):
    if(len(img.shape) > 2):
        h, w, c = img.shape
    else:
        h, w = img.shape
    r = new_width / w
    dim = (new_width, int(h * r))
    img = cv2.resize(img, dim, interpolation = cv2.INTER_LINEAR)
    return img

file_names = ['control.jpg']

for file_name in file_names:

	# load image in grayscale
	img = cv2.imread(file_name, 0)

	# resize image
	img = resize(img, 300)

	# compute x-gradient
	sobel_x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize = 3)
	sobel_x = cv2.normalize(sobel_x, sobel_x, -127.0, 127.0, cv2.NORM_MINMAX, cv2.CV_8S)
	cv2.imshow('sobelx', sobel_x)

	# compute y-gradient
	sobel_y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize = 3)
	sobel_y = cv2.normalize(sobel_y, sobel_y, -127.0, 127.0, cv2.NORM_MINMAX, cv2.CV_8S)
	cv2.imshow('sobely', sobel_y)

	

	# make matrix of gradient vectors
	# for row in len(img):
		

	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# for row in img:
	# 	for c in row:
	# 		for 