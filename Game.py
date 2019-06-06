# This is the general program flow and game execution
class Ship:
    def __init__(self, image, parent_board, length, direction):
        from PIL import ImageTk, Image
        self.imageTk = ImageTk.PhotoImage(image)
        self.length = length
        self.parentBoard = parent_board
        self.direction = direction

    def check_place(self, xcoord, ycoord):
        can_place = True
        for i in range(self.length):
            if self.direction == 0 and xcoord < 10 and ycoord + i < 10:
                if playerBoard[xcoord][ycoord + i] != " ":
                    can_place = False
                    break
            elif self.direction == 1 and xcoord + i < 10 and ycoord < 10:
                if playerBoard[xcoord + i][ycoord] != " ":
                    can_place = False
                    break
            else:
                can_place = False
                break
        return can_place

    def board_place(self, xcoord, ycoord):
        import UIControl
        from tkinter import NW
        if self.check_place(xcoord, ycoord):
            for i in range(self.length):
                if self.direction == 0:
                    playerBoard[xcoord][ycoord + i] = "S"
                else:
                    playerBoard[xcoord + i][ycoord] = "S"
            self.parentBoard.create_image(UIControl.BOX_WIDTH * xcoord + UIControl.BOX_OFFSET, UIControl.BOX_HEIGHT *
                                          ycoord + UIControl.BOX_OFFSET, image=self.imageTk, anchor=NW)


def setup_game():
    global AIBoard, playerBoard
    base_board = []
    for i in range(10):  # This creates the stock board
        base_board.append([])
        for j in range(10):
            base_board[i].append(" ")
    AIBoard = base_board
    playerBoard = base_board


def start_game():
    global difficulty, AI
    import AIControl, UIControl
    difficulty = UIControl.difficulty
    AI = AIControl.AI(difficulty)
