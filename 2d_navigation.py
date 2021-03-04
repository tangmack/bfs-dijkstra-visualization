import numpy as np
import cv2
world_map = np.zeros((300,400),dtype=np.uint8)

def convert_row_to_y(row, img_height):
    return img_height - row

def convert_y_to_row(y, img_height):
    return img_height - y

def convert_col_to_x(col):
    return col

# lines in y = mx + b format
L = np.array([[124.3830,	-1.468345131,	35.5285,	176.5511],
                 [124.3830,	0.740180419,	35.5285,	98.0855],
                 [194.0365,	0.700207991,	170.8728,	74.3900],
                 [194.0365,	-1.428147722,	170.8728,	438.0681],
                 [105.4264,	1,	285.5736,	-180.1472],
                 [137.2948,	-0.298786326,	351.0415,	242.1812],
                 [137.2948,	1.124925401,	351.0415,	-257.6007],
                 [116.0330,	1,	381.0330,	-265.0000],
                 [105.4264,	-1,	285.5736,	391.0000]])

m = L[:,1]
b = L[:,3]

img_height = world_map.shape[0]

for row in range(0, world_map.shape[0]):
    for col in range(0, world_map.shape[1]):
        x = col
        y = convert_row_to_y(row, world_map.shape[0])

        if (y > m[0]*x + b[0]) and (y < m[1]*x + b[1]) and (y > m[2]*x + b[2]) and (y < m[3]*x + b[3]):
            world_map[convert_y_to_row(y,img_height),x] = 255

cv2.imshow("world_map", world_map)
cv2.waitKey(0)



