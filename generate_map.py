import numpy as np
import cv2

def convert_row_to_y(row, img_height):
    return img_height - row

def convert_y_to_row(y, img_height):
    return img_height - y

def convert_col_to_x(col):
    return col

def create_map():
    world_map = np.zeros((300, 400), dtype=np.uint8)

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

            if (y > m[0]*x + b[0]) and (y < m[1]*x + b[1]) and (y > m[2]*x + b[2]) and (y < m[3]*x + b[3]): # Rectangle
                world_map[convert_y_to_row(y,img_height),x] = 255

            elif (x-90)**2 + (y - 70)**2 < 35**2: # Circle
                world_map[convert_y_to_row(y, img_height), x] = 255

            elif y < 280 and y > 230 and x > 200 and ( x<210 or (y>270 and x<230) or (y<240 and x<230) ): # Channel shape
                world_map[convert_y_to_row(y, img_height), x] = 255

            elif (x-246)**2/60**2 + (y-145)**2/30**2 < 1: # Ellipse
                world_map[convert_y_to_row(y, img_height), x] = 255

            elif (y < m[4]*x + b[4]) and (y < m[5]*x + b[5]) and (y > m[6]*x + b[6]) and (y > m[8]*x + b[8]) or (y < m[6]*x + b[6]) and (x<381.0330) and (y > m[7]*x + b[7]) and (y > m[8]*x + b[8]): # Polyhedron
                world_map[convert_y_to_row(y, img_height), x] = 255

    return world_map

if __name__ == '__main__':
    world_map = create_map()

    cv2.imshow("world_map", world_map)
    cv2.waitKey(0)