from jpeg_creator import *

# board = generate_board()

sample_input  =  [[0 for col in range(N_BLOCKS)] for row in range(N_BLOCKS)]
sample_input[0][0] = 4
sample_input[2][1] = 2
sample_input[5][2] = 3
sample_input[3][3] = 5
sample_input[6][4] = 6
sample_input[7][5] = 3
sample_input[7][6] = 2
sample_input[1][7] = 4
sample_input[6][0] = 1
sample_input[1][1] = 1
sample_input[2][2] = 1
sample_input[3][3] = 1
sample_input[6][4] = 1
sample_input[7][5] = 1
sample_input[0][6] = 1
sample_input[2][7] = 1

sample_input[-8][0] = -4
sample_input[-2][1] = -2
sample_input[-5][2] = -3
sample_input[-3][3] = -5
sample_input[-6][4] = -6
sample_input[-7][5] = -3
sample_input[-7][6] = -2
sample_input[-1][7] = -4
sample_input[-6][0] = -1
sample_input[-1][1] = -1
sample_input[-2][2] = -1
sample_input[-3][3] = -1
sample_input[-6][4] = -1
sample_input[-7][5] = -1
sample_input[-8][6] = -1
sample_input[-2][7] = -1

# board = place_icons(board, sample_input)
# cv2.imwrite("generated_img.png",board)