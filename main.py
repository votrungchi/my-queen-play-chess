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
import asyncio
import chess
import chess.engine
import cv2

from move_detection import move_detect
from config import setup, image_capture, draw_square, human, engine_path

def main():
    setup()

    draw_img = image_capture()
    cv2.imshow("My Queen Play Chess", draw_img)

    board = chess.Board(fen=chess.STARTING_BOARD_FEN) # object of chess board
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    move = chess.Move.null()
    old_square = -1
    new_square = -1

    while not board.is_game_over():
        if (board.turn == human):
            img_1 = image_capture()

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

            move, old_square, new_square = move_detect(img_1, img_2, board.fen(), board.turn)

        else:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            move = result.move
            old_square = chess.square_mirror(move.from_square)
            new_square = chess.square_mirror(move.to_square)
            # show AI move
            draw_img = img_2.copy()
            draw_square(draw_img, old_square, color=(0, 0, 255))
            draw_square(draw_img, new_square, color=(0, 255, 0))
            cv2.imshow("My Queen Play Chess", draw_img)

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
            # show AI moved
            img_2 = image_capture()
            draw_img = img_2.copy()
            draw_square(draw_img, old_square, color=(0, 0, 255))
            draw_square(draw_img, new_square, color=(0, 255, 0))
            cv2.imshow("My Queen Play Chess", draw_img)

        if move != chess.Move.null() and move in board.legal_moves:
            board.push(move)
            # show game
            draw_img = img_2.copy()
            draw_square(draw_img, old_square, color=(0, 0, 255))
            draw_square(draw_img, new_square, color=(0, 255, 0))
            cv2.imshow("My Queen Play Chess", draw_img)
        else:
            print("Revert move and press 'r' to start remote")
            while True:
                if cv2.waitKey(1) == ord('r'):
                    break

    print("game over!")
    cv2.waitKey(0)

if __name__ == "__main__":
    main()