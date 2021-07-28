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

import cv2
import numpy as np
import chess
from config import square_size

def fen2board_bitmap(fen, turn):
    board_bitmap = []
    for row in reversed(fen.split(' ')[0].split('/')):
        for square in list(row):
            if square.isnumeric():
                for i in range(int(square)):
                    board_bitmap.append(0)
            else:
                if (turn == chess.WHITE):
                    if square.isupper():
                        board_bitmap.append(1)
                    else:
                        board_bitmap.append(0)
                else:
                    if square.islower():
                        board_bitmap.append(1)
                    else:
                        board_bitmap.append(0)

    board_bitmap = np.array(board_bitmap)
    return board_bitmap

def move_detect(img_old, img_new, fen, turn):
    board_bitmap = fen2board_bitmap(fen, turn)

    image_diff = cv2.absdiff(img_old, img_new)
    image_diff_gray = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(image_diff_gray, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow("diff", image_diff)
    # cv2.imshow("diff_gray", image_diff_gray)
    # cv2.imshow("threshold", threshold)

    if len(contours) >= 2:
        selected_contours_mid_point = []
        area_list = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > 0:
                area_list.append([area, c])

        # select two contours which have the largest area
        area_list.sort(key=lambda tup: tup[0], reverse=True)
        for area in area_list[:2]:
            (x, y, w, h) = cv2.boundingRect(area[1])
            selected_contours_mid_point.append([x + int(w/2), y + int(h/2)])

        old_square = -1
        new_square = -1

        for mid_point in selected_contours_mid_point:
            square = int((mid_point[0] / square_size)) + (8 * int(8 - (mid_point[1] / square_size)))
            print(square)
            if (board_bitmap[square] == 1):
                old_square = square
            else:
                new_square = square

        # move detected
        print(old_square, new_square)
        move_notation = chess.square_name(old_square) + chess.square_name(new_square)
        print(move_notation)

        return move_notation, old_square, new_square
    else:
        return " ", -1, -1
