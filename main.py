from numpy import *
from cv2 import *

from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()

input_file = filedialog.askopenfilename()
image = imread(input_file, 0)

im_width, im_height = image.shape

# Create a blank 300x300 black image
output_im = zeros((im_width, im_height, 3), uint8)
output_im[:] = (255, 255, 255)
output_masked = output_im.copy()

output_masked = bitwise_and(output_im, output_im, mask=image)
namedWindow("Processing", WINDOW_NORMAL)
start_location = (0, 0)
imshow('Processing', output_masked)
waitKey(1)

# find the first black pixel
for x in range(0, im_width):
    for y in range(0, im_height):
        new_im = output_masked.copy()
        if image[x, y] == 0:
            start_location = (x, y)
            break
        new_im[x, y] = (0, 0, 255)
        # imshow('Processing', new_im)

        #if waitKey(1) == ord('q'):
        #    break
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
points = []
search_multiplier = 1
points.append(start_location)
print("starting search")
print(points)
while searching:
    x, y = points[-1]
    output_masked[x - 1 : x + 1 , y - 1 : y + 1] = (0, 255, 0)
    imshow("Processing", output_masked)
    if waitKey(1) == ord('q'):
      searching = False

    no_of_points_at_start = len(points)
    was_white = False
    #look at adjacent bits
    scaled_search_pattern = map(lambda li: (search_multiplier * li[0], search_multiplier * li[1]), search_pattern)
    for (adj_x, adj_y) in scaled_search_pattern:
        current_try = (x + adj_x, y + adj_y)
        if image[current_try] == 255:
            was_white = True

        if image[x + adj_x, y + adj_y] == 0 and was_white:
            if current_try not in points[:-2]:
                search_multiplier = 1
                points.append(current_try)
            break

        if len(points) > 1 and current_try == points[0]:
            searching = False

    if len(points) == no_of_points_at_start:
      search_multiplier += 1


destroyAllWindows()

output_file = filedialog.asksaveasfilename()
if output_file != "":
    with open(output_file, "w") as f:
        f.write("polygon(points = [")
        for (x, y) in points:
            f.write("[" + str(x) + "," + str(y) + "],")
        f.write("]);")
