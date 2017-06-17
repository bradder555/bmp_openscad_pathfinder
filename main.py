from numpy import *
from cv2 import *

from tkinter import Tk
from tkinter import filedialog
import os
import time

root = Tk()
root.withdraw()

input_file = filedialog.askopenfilename()

image = imread(input_file, 0)
print(image[0, 0])

im_width, im_height = image.shape

# Create a blank 300x300 black image
output_im = zeros((im_width, im_height, 3), uint8)
output_im[:] = (255, 255, 255)
output_masked = output_im.copy()

output_masked = bitwise_and(output_im, output_im, mask=image)
namedWindow("Processing", WINDOW_NORMAL)
start_location = (0, 0)

# find the first black pixel
for x in range(0, im_width):
    for y in range(0, im_height):
        new_im = output_masked.copy()
        if image[x, y] == 0:
            start_location = (x, y)
            break
        new_im[x, y] = (0, 0, 255)
        imshow('Processing', new_im)

        if waitKey(1) == ord('q'):
            break
    else:
        continue
    break

search_pattern = [(-1, -1),
                  (-1, 0),
                  (-1, 1),
                  (0, 1),
                  (1, 1),
                  (1, 0),
                  (1, -1),
                  (0, -1),
                  (-1, -1)]

searching = True
cursor_location = start_location
points = []
while searching:
    x, y = cursor_location
    points.append(cursor_location)
    was_light = False
    last_tried = ()
    #look at adjacent bits
    for (adj_x, adj_y) in search_pattern:
        current_try = (x + adj_x, y + adj_y)
        print(current_try)
        if image[current_try] == 255:
            print("white")
            was_light = True
            last_try = current_try

        if image[x + adj_x, y + adj_y] == 0 and was_light:
            print("black")
            cursor_location = current_try
            break

        if cursor_location == start_location and len(points) > 1:
            searching = False

        new_im = output_masked.copy()
        new_im[current_try] = (255, 0, 0)
        output_masked[cursor_location] = (255, 0, 0)
        imshow("Processing", new_im)

        if waitKey(1) == ord('q'):
            searching = False
            break

destroyAllWindows()

output_file = filedialog.asksaveasfilename()

with open(output_file, "w") as f:
    f.write("polygon(points = [")
    for (x, y) in points:
        f.write("[" + str(x) + "," + str(y) + "],")
    f.write("]);")
