## Set of methods used to transform images in the QOI benchmark set
## Relies heavily on Pillow (python imaging library): https://pillow.readthedocs.io/en/stable/
from PIL import Image
import numpy as np
import os

# Helper to increment pixel array dimensions
def counter(size,row,column):
    if column == size - 1:
        column = 0; row += 1
    else:
        column += 1
    return row,column

# Scans in a 2x2 "U"
def u_scan(img):
    img_array = np.array(img)
    size = int(img_array.shape[0])
    new_img = np.zeros((size,size,3), dtype=np.uint8)
    row = 0; old_row = 0; column = 0; old_column = 0
    while (old_row < size):
        while (old_column < size):
            new_img[row][column] = img_array[old_row][old_column]; row,column = counter(size,row,column)        #origin
            new_img[row][column] = img_array[old_row+1][old_column]; row,column = counter(size,row,column);     #down
            new_img[row][column] = img_array[old_row+1][old_column+1]; row,column = counter(size,row,column);   #right
            new_img[row][column] = img_array[old_row][old_column+1]; row,column = counter(size,row,column);     #up
            old_column+=2
        old_row += 2 #move to next row
        old_column = 0 #reset columns
    return(Image.fromarray(new_img))

# Scans down, up... 
def raster_scan(img):
    img_array = np.array(img)
    size = int(img_array.shape[0])
    new_img = np.zeros((size,size,3), dtype=np.uint8)
    row = 0; old_row = 0; column = 0; old_column = 0
    invert = 1  #track if this is an "up" or a "down" case
    while(old_column < size):
        if(invert):
            invert = 0
            old_row = 0
        else:
            invert = 1
            old_row = size - 1
        for i in range(size):
            new_img[row][column] = img_array[old_row][old_column]; row,column = counter(size,row,column)    #move along column
            if (invert):
                old_row -= 1
            else:
                old_row += 1
        old_column += 1
    return(Image.fromarray(new_img))

# Explores 4x4 neighbourhoods
def orthogonal_scan(img):
    img_array = np.array(img)
    size = int(img_array.shape[0])
    new_img = np.zeros((size,size,3), dtype=np.uint8)
    row = 0; old_row = 0; column = 0; old_column = 0
    while(old_row < size):
        while(old_column < size):
            new_img[row][column] = img_array[old_row][old_column]; row,column = counter(size,row,column)      # origin
            new_img[row][column] = img_array[old_row+1][old_column]; row,column = counter(size,row,column)    # down
            new_img[row][column] = img_array[old_row+1][old_column+1]; row,column = counter(size,row,column)  # right
            new_img[row][column] = img_array[old_row][old_column+1]; row,column = counter(size,row,column)    # up
            new_img[row][column] = img_array[old_row][old_column+2]; row,column = counter(size,row,column)    # right
            new_img[row][column] = img_array[old_row+1][old_column+2]; row,column = counter(size,row,column)  # down
            new_img[row][column] = img_array[old_row+2][old_column+2]; row,column = counter(size,row,column)  # down
            new_img[row][column] = img_array[old_row+2][old_column+1]; row,column = counter(size,row,column)  # left
            new_img[row][column] = img_array[old_row+2][old_column]; row,column = counter(size,row,column)    # left
            new_img[row][column] = img_array[old_row+3][old_column]; row,column = counter(size,row,column)    # down
            new_img[row][column] = img_array[old_row+3][old_column+1]; row,column = counter(size,row,column)  # right
            new_img[row][column] = img_array[old_row+3][old_column+2]; row,column = counter(size,row,column)  # right
            new_img[row][column] = img_array[old_row+3][old_column+3]; row,column = counter(size,row,column)  # right
            new_img[row][column] = img_array[old_row+2][old_column+3]; row,column = counter(size,row,column)  # up
            new_img[row][column] = img_array[old_row+1][old_column+3]; row,column = counter(size,row,column)  # up
            new_img[row][column] = img_array[old_row][old_column+3]; row,column =counter(size,row,column)     # up
            old_column+=4
        old_row += 4
        old_column = 0
    return(Image.fromarray(new_img))