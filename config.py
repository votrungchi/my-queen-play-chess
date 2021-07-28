"""
MIT License

Copyright (c) 2021 Vo Trung Chi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import errno
import cv2
import numpy as np
import chess

video_source = 'http://192.168.1.4:8080/video'
resolution = (800, 800)
board_size, _ = resolution
square_size = int(board_size / 8)

config_path = os.path.dirname(os.path.realpath(__file__)) + "/config" # path of current directory

player_color = chess.WHITE

# initialize variable for config board perspective
img = 0
ix, iy = -1, -1

pts1 = np.float32([[0,0], [0, 0], [0, 0], [0, 0]])
pts2 = np.float32([[0,0], [0, 0], [0, 0], [0, 0]])

def setup():
    global pts1
    global pts2

    if not os.path.exists(config_path):
        try:
            os.makedirs(config_path)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # get_board_perspective()
    pts1 = np.load(config_path + '/chess_board_warp_perspective.npz')['pts1']
    pts2 = np.load(config_path + '/chess_board_warp_perspective.npz')['pts2']


def draw_square(img, square, color=(0, 0, 0), thickness=3):
    # calculate box location to draw the move
    box = [((square % 8) * square_size, board_size - (int(square / 8) + 1) * square_size), # x
              (((square % 8) + 1) * square_size, board_size - int(square / 8) * square_size)] # y
    cv2.rectangle(img, box[0], box[1], color=color, thickness=thickness)

def draw_circle(event, x, y, flags, param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x,y), 2, (255, 0, 0), -1)
        ix, iy = x, y

def get_points(image, numOfPoints):
    global img
    img = image.copy()
    img = cv2.resize(img, resolution)

    # width, height = image.shape[:2]
    cv2.namedWindow("Perspective")
    cv2.setMouseCallback("Perspective", draw_circle)

    points = []
    print("Press 'a' for add point : ")

    while len(points) != numOfPoints:
        cv2.imshow("Perspective", img)
        k = cv2.waitKey(1)
        if k == ord('a'):
            points.append([int(ix), int(iy)])
            cv2.circle(img, (ix, iy), 3, (0, 0, 255), -1)

    cv2.destroyAllWindows()
    return list(points)

def image_capture():
    _, img = cv2.VideoCapture(video_source).read()
    img = cv2.resize(img, resolution)
    img = get_warp_img(img, config_path, resolution)
    return img

def get_warp_img(img, config_path, resolution):
    h, _ = cv2.findHomography(pts1, pts2)
    result = cv2.warpPerspective(img, h, resolution)
    return result

def get_board_perspective():
    global pts1
    global pts2

    ret, img = cv2.VideoCapture(video_source).read()
    img = cv2.resize(img, resolution)
    width, height = resolution

    warp_points = get_points(img, 4)

    pts1 = np.float32([[warp_points[0][0], warp_points[0][1]],
                      [warp_points[1][0], warp_points[1][1]],
                      [warp_points[3][0], warp_points[3][1]],
                      [warp_points[2][0], warp_points[2][1]]])
    pts2 = np.float32([[0,0], [width, 0], [0, height], [width, height]])

    np.savez(config_path + "/chess_board_warp_perspective.npz", pts1=pts1, pts2=pts2)

    result = get_warp_img(img, config_path, resolution)
    for square in range(64):
        draw_square(result, square, color=(0, 0, 255))
    cv2.imshow("Perspective result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()