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

import chess
import chess.engine
import cv2

from move_detection import move_detect
from config import setup, image_capture, draw_square

board = chess.Board(fen=chess.STARTING_BOARD_FEN) # object of chess board

def main():
    setup()

    draw_img = image_capture()
    cv2.imshow("My Queen Play Chess", draw_img)

    while True:
        img_1 = image_capture()
        # cv2.imshow("start", img_1)

        if (board.turn == chess.WHITE):
            print("White move: ")
            print("Press 'w' when done.")
            while True:
                if cv2.waitKey(1) == ord('w'):
                    break
        else:
            print("Black move: ")
            print("Press 'b' when done.")
            while True:
                if cv2.waitKey(1) == ord('b'):
                    break

        img_2 = image_capture()
        # cv2.imshow("img", img_2)

        move_notation, old_square, new_square = move_detect(img_1, img_2, board.fen(), board.turn)
        if (move_notation and old_square != -1 and new_square != -1):
            # show game
            draw_img = img_2.copy()
            draw_square(draw_img, old_square, color=(0, 0, 255))
            draw_square(draw_img, new_square, color=(0, 255, 0))
            cv2.imshow("My Queen Play Chess", draw_img)

            move = chess.Move.from_uci(str(move_notation))
            if move in board.legal_moves:
                board.push(move)
                print("done")
        else:
            print("Revert move and press 'r' to start remote")
            while True:
                if cv2.waitKey(1) == ord('r'):
                    break

    cv2.waitKey(0)

if __name__ == "__main__":
    main()