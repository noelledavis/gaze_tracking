# find_iris_center.py
# Find iris center from eye image.

from __future__ import division
import math
import cv2
import numpy as np
from numpy import linalg as LA
import itertools
import timeit # for testing

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

# calculate magnitude of 2-D vector
def normalize(x, y, threshold = 0):
	mag = math.sqrt(x ** 2 + y ** 2)
	if mag > 0:
		return [x / mag, y / mag]
	else:
		return [0, 0]

file_names = ['eye0.jpg']

for file_name in file_names:

	# load image in grayscale
	img = cv2.imread(file_name, 0)

	# resize image
	img = resize(img, 20)
	h, w = img.shape

	# compute x-gradient
	sobel_x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize = 3)
	sobel_x = cv2.normalize(sobel_x, sobel_x, -127.0, 127.0, cv2.NORM_MINMAX, cv2.CV_8S)
	# cv2.imshow('sobelx', sobel_x)

	# compute y-gradient
	sobel_y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize = 3)
	sobel_y = cv2.normalize(sobel_y, sobel_y, -127.0, 127.0, cv2.NORM_MINMAX, cv2.CV_8S)
	# cv2.imshow('sobely', sobel_y)

	start = timeit.default_timer()

	# normalize and threshold gradient vectors
	grad_x = []
	grad_y = []

	for (x_row, y_row) in itertools.izip(sobel_x, sobel_y): # using itertools is marginally faster than looping through indices

		for (x, y) in itertools.izip(x_row, y_row):

			# normalize gradient vector
			norm = normalize(x, y, threshold = 0)

			grad_x.append(norm[0])
			grad_y.append(norm[1])

	grad_x = np.reshape(np.array(grad_x, dtype = np.float16), (-1, w))
	grad_y = np.reshape(np.array(grad_y, dtype = np.float16), (-1, w))

	grad = np.dstack((grad_x, grad_y))

	# find center
	max_dot_sum = -1

	for (center_r, center_c) in np.ndindex(h, w):
		
		dot_sum = 0

		for (grad_r, grad_c) in np.ndindex(h, w):

			disp = normalize(grad_r - center_r, grad_c - center_c)

			dot = disp[0] * grad_y[grad_r, grad_c] + disp[1] * grad_x[grad_r, grad_c]
			
			dot_sum += dot
		
		if dot_sum > max_dot_sum:
			max_dot_sum = dot_sum
			center = [center_c, center_r]

	print 'center:', center

	print 'elapsed time:', timeit.default_timer() - start

	cv2.circle(img, tuple(center), 1, 255, -1)

	cv2.imshow('img', img)

	cv2.waitKey(0)
	cv2.destroyAllWindows()