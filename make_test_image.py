# make_test_image.py
# Create rough image of an eye to use as a control when testing.

import cv2
import numpy as np

def create_blank(width = 500, height = 500, rgb_color = (255, 255, 255)):
	""" Create new image (numpy array) filled with a certain rgb color """

	# create blank black image
	img = np.zeros((height, width, 3), np.uint8)

	# since opencv uses bgr, convert color first
	color = tuple(reversed(rgb_color))

	# fill image with color
	img[:] = color

	return img

# create blank white image
control = create_blank()

# add a black circle to represent iris
cv2.circle(control, (250, 250), 200, (0, 0, 0), -1)

# show image
cv2.imshow('control', control)

# save image
cv2.imwrite('control.jpg', control)

# wait for keypress then close image window
cv2.waitKey(0)
cv2.destroyAllWindows()