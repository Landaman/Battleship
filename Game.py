# This is the general program flow and game execution
AIBoard = None
AI = None
playerBoard = None
playerTurn = None
gameRunning = True


class Ship:
    def __init__(self, parent_container, parent_board, parent_canvas, length, direction, image):
        from PIL import ImageTk
        self.imageTk = ImageTk.PhotoImage(image)
        self.length = length
        self.container = parent_container
        self.parentCanvas = parent_canvas
        self.parentBoard = parent_board
        self.direction = direction
        self.xcoord = None
        self.ycoord = None

    def check_place(self, xcoord, ycoord):
        can_place = True
        for i in range(self.length):
            if self.direction == 0 and xcoord < 10 and ycoord + i < 10:
                if self.parentBoard[xcoord][ycoord + i] != " ":
                    can_place = False
                    break
            elif self.direction == 1 and xcoord + i < 10 and ycoord < 10:
                if self.parentBoard[xcoord + i][ycoord] != " ":
                    can_place = False
                    break
            else:
                can_place = False
                break
        return can_place

    def board_place(self, xcoord, ycoord):
        import UIControl
        import tkinter as tk
        if self.check_place(xcoord, ycoord):
            self.xcoord = xcoord
            self.ycoord = ycoord
            for i in range(self.length):
                if self.direction == 0:
                    self.parentBoard[xcoord][ycoord + i] = "S"
                else:
                    self.parentBoard[xcoord + i][ycoord] = "S"
            self.parentCanvas.create_image(UIControl.BOX_WIDTH * xcoord + UIControl.BOX_OFFSET, UIControl.BOX_HEIGHT *
                                           ycoord + UIControl.BOX_OFFSET, image=self.imageTk, anchor=tk.NW)

    def check_health(self):
        import tkinter as tk
        import UIControl
        damage = 0
        if self.direction == 0:
            for i in range(self.length):
                if self.parentBoard[self.xcoord][self.ycoord + i] == "H":
                    damage += 1
        else:
            for i in range(self.length):
                if self.parentBoard[self.xcoord + i][self.ycoord] == "H":
                    damage += 1
        if damage == self.length:
            self.container.remove(self)
            if len(self.container) == 0:
                winner()


def winner():
    import UIControl
    if len(UIControl.board.playerShips) == 0:
        UIControl.setup_victory("The AI")
    else:
        UIControl.setup_victory("The player")


def ai_move(xcoord, ycoord):
    import UIControl
    if not playerTurn and gameRunning:
        hit = False
        if playerBoard[xcoord][ycoord] == "S" or playerBoard[xcoord][ycoord] == "H":
            hit = True
            playerBoard[xcoord][ycoord] = "H"
            for i in UIControl.board.playerShips:
                i.check_health()
        else:
            playerBoard[xcoord][ycoord] = "M"
        UIControl.board.show_ai_move(xcoord, ycoord, hit)


def player_move(xcoord, ycoord):
    import UIControl
    global AI
    if playerTurn and gameRunning:
        hit = False
        if AIBoard[xcoord][ycoord] == "S" or AIBoard[xcoord][ycoord] == "H":
            hit = True
            AIBoard[xcoord][ycoord] = "H"
            for i in AI.ships:
                i.check_health()
        else:
            AIBoard[xcoord][ycoord] = "M"
        UIControl.board.show_player_move(xcoord, ycoord, hit)


def setup_game():
    global AIBoard, playerBoard
    playerBoard = []
    AIBoard = []
    for i in range(10):  # This creates the stock board
        playerBoard.append([])
        for j in range(10):
            playerBoard[i].append(" ")
    for i in range(10):  # This creates the stock board
        AIBoard.append([])
        for j in range(10):
            AIBoard[i].append(" ")


def start_game():
    global difficulty, AI, playerTurn
    import AIControl
    import UIControl
    difficulty = UIControl.difficulty
    AI = AIControl.AI(difficulty)
    AI.gen_board()
    UIControl.board.actionLabel.configure(text="Choose a target:")
    UIControl.board.show_ai_board()
    playerTurn = True
