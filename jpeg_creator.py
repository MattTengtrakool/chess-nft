#!/bin/python3

import cv2
import numpy as np

n_blocks = 8
block_dim = 75
image_dim = block_dim * n_blocks


dark_brown = (99, 136, 181)
light_brown = (181, 217, 240)

blank_image = np.zeros((image_dim, image_dim, 3), np.uint8)



# find a smarter way to do this
for row in range(n_blocks):
    for col in range (row % 2, n_blocks, 2):
        row_start = row * block_dim
        col_start = col * block_dim
        blank_image[row_start : row_start + block_dim, 
            col_start: col_start + block_dim] = light_brown
    for col in range (row % 2 - 1, n_blocks, 2):
        if (col < 0):
            continue
        row_start = row * block_dim
        col_start = col * block_dim
        blank_image[row_start : row_start + block_dim, 
            col_start: col_start + block_dim] = dark_brown

cv2.imshow("board", blank_image)
cv2.waitKey()
cv2.destroyAllWindows()
