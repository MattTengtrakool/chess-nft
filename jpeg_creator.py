#!/bin/python3

import cv2
import numpy as np
from constants import *

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    """
    @overlay_transparent     Overlays a transparant PNG onto another image using CV2

    @param      background_img    The background image
    @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
    @param      x                 x location to place the top-left corner of our overlay
    @param      y                 y location to place the top-left corner of our overlay
    @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None

    @return     Background image with overlay on top
    """

    bg_img = background_img.copy()

    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size, interpolation = cv2.INTER_AREA)

    # Extract the alpha mask of the RGBA image, convert to RGB 
    b,g,r,a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b,g,r))

    h, w, _ = overlay_color.shape
    roi = bg_img[y:y+h, x:x+w]

    # Black-out the area behind the logo in our original ROI
    # The mask allows us to ignore non transparent part
    # while we add the other part, so this overlays the image with just black
    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(a)) 

    

    # Mask out the logo from the logo image.
    # isolate only the colored part of the image using the alphas as a mask
    # and remove everything else that has no color
    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = a)
  
    # Update the original image with our new ROI
    # Add the image with the shape cut out and the colored image with 
    # a shape, forming the merged image
    bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

    return bg_img

def generate_board(b_width = BLOCK_DIM, b_height = BLOCK_DIM, x_n_blocks = N_BLOCKS, y_n_blocks = N_BLOCKS):
    """
    @generate_board                      Generates an image with a chess board pattern
    
    @param          b_width              The width of each square 
    @param          b_height             The height of each square
    @param          x_n_blocks           The number of blocks in the horizontal direction
    @param          y_n_blocks           The number of blocks in the vertcal direction       
    """
    
    width = b_width * x_n_blocks
    height = b_height * y_n_blocks
    
    board = np.zeros((width, height, 3), np.uint8)
    
    for row in range(y_n_blocks):    
        # Color the light squares
        for col in range (x_n_blocks):
            row_start = row * b_height
            col_start = col * b_width
            if ((row + col) % 2 == 0):
                board[row_start : row_start + b_height, 
                    col_start: col_start + b_width] = LIGHT_BROWN
            else:
                board[row_start : row_start + b_height, 
                    col_start: col_start + b_width] = DARK_BROWN
    return board

def place_icons(board, instruction, b_height = BLOCK_DIM, b_width = BLOCK_DIM, scale = 0.7):
    
    """
    @place_icons    Places images in a another image according to the mapping defined in PIECE_MAP
                    and it assumes the underlying image is a checker board patter with a hieght of
                    b_height and a width of b_width
                    
    @param      board            Checker board image to be used as a background
    @param      instruction      Location information about where to locate different pieces, as defined
                                 by PIECE map
    @param      b_height         The height of a square in the checker pattern
    @param      b_width          The width of a square in the cherker pattern
    @param      scale            By how much should the images being overlayed scaled
    """
    
    board = board.copy()
    for row in range(len(instruction)):
        for col in range (len(instruction[row])):
            val = instruction[row][col]
            if (abs(val) in PIECE_MAP):
                color = "w" if val < 0 else "b"
                icon_name = f"icons/{color}{PIECE_MAP[abs(val)]}.png"

                icon = cv2.imread(icon_name, cv2.IMREAD_UNCHANGED)
            
                # Add icon at its location
                row_start = row * b_height + int((1 - scale) * b_height)
                col_start = col * b_width  + int(((1 - scale) * b_width)/2)
                board = overlay_transparent(board, icon, col_start, row_start, (int(b_width * scale), int(b_height * scale)))
    return board
    

board = generate_board()
cv2.imshow("board", board)

sample_input  =  [[0 for col in range(N_BLOCKS)] for row in range(N_BLOCKS)]
sample_input[0][1] = 1
sample_input[0][2] = 2
sample_input[0][3] = 3
sample_input[0][4] = 4
sample_input[0][5] = 5
sample_input[0][6] = 6
sample_input[-1][1] = -1
sample_input[-1][2] = -2
sample_input[-1][3] = -3
sample_input[-1][4] = -4
sample_input[-1][5] = -5
sample_input[-1][6] = -6

board = place_icons(board, sample_input)



cv2.imshow("Board", board)
cv2.waitKey()
cv2.destroyAllWindows()



