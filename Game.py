# This is the general program flow and game execution
AIBoard = None
AI = None
playerBoard = None
playerTurn = None
gameRunning = True


class Ship:
    # This is the basic ship class. It can manage its own VALID placement on the canvas, and manages its own deletion
    # when it runs out of health.
    def __init__(self, parent_container, parent_board, parent_canvas, length, direction, image):
        # parent_container is the array that holds the ships. parent_board is the board array that the ship is a
        # part of, parent_canvas is the canvas that the ships is to be placed on, length is the length is the length
        # of the ship, direction is 0 for vertical, 1 for horizontal, and image is the opened image of image the
        # ship should use.
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
        # This ensures a valid placement, and will return a bool of whether the ship can be placed there or not.
        # xcoord is the X coordinate for the ship(the leftmost point if the ship is horizontal),
        # ycoord is the Y coordinate for the top of the ship(the ship in general if its horizontal).
        can_place = True
        for i in range(self.length):  # This scans the board for obstacles in the way of placement.
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
        # This manages placement on the board. It first checks the placement with the self.check_place() function
        # then will make an image of itself an update the appropriate board array. xcoord is the X coordinate for the
        # ship(the leftmost point if the ship is horizontal), ycoord is the Y coordinate for the top of the ship(the
        # ship in general if its horizontal).
        import UIControl
        import tkinter as tk
        if self.check_place(xcoord, ycoord):
            self.xcoord = xcoord
            self.ycoord = ycoord
            for i in range(self.length):  # This updates the board to make a placed ship.
                if self.direction == 0:
                    self.parentBoard[xcoord][ycoord + i] = "S"
                else:
                    self.parentBoard[xcoord + i][ycoord] = "S"
            self.parentCanvas.create_image(UIControl.BOX_WIDTH * xcoord + ((xcoord + 1) * UIControl.BOX_OFFSET),
                                           UIControl.BOX_HEIGHT * ycoord + ((ycoord + 1) * UIControl.BOX_OFFSET),
                                           image=self.imageTk, anchor=tk.NW)

    def check_health(self):
        # This scans every space that the ships is supposed to occupy for hits, and if the hits are equal to the ships
        # length, the ship will delete itself.
        damage = 0
        if self.direction == 0:  # This scans the board for hits in occupied space.
            for i in range(self.length):
                if self.parentBoard[self.xcoord][self.ycoord + i] == "H":
                    damage += 1
        else:
            for i in range(self.length):
                if self.parentBoard[self.xcoord + i][self.ycoord] == "H":
                    damage += 1
        if damage == self.length:  # This checks if the ship has been destroyed
            self.container.remove(self)
            if len(self.container) == 0:
                # This scans for a potential winner. If the container holding the ships is empty, all ships have
                # been destroyed.
                winner()


def winner():
    # This function should be run whenever check_health() finds that a player has lost. It will find whatever player
    # had lost, then the win screen with the appropriate name.
    import UIControl
    if len(UIControl.board.playerShips) == 0:  # This scans for who has won
        UIControl.setup_victory("The AI")
    else:
        UIControl.setup_victory("The player")


def ai_move(xcoord, ycoord):
    # This function will determine an AI move as a hit or miss, update the board and then display that on the canvas,
    # given the x and y coordinates of the move, the fact that it isn't the players turn and a winner hasn't been
    # declared. If a hit is found, the players ships will check their health to see if they've been destroyed.
    import UIControl
    if not playerTurn and gameRunning:
        hit = False
        if playerBoard[xcoord][ycoord] == "S" or playerBoard[xcoord][ycoord] == "H":  # This checks the board.
            hit = True
            playerBoard[xcoord][ycoord] = "H"
            for i in UIControl.board.playerShips:  # This checks all of the players ships health.
                i.check_health()
        else:
            playerBoard[xcoord][ycoord] = "M"
        UIControl.board.show_ai_move(xcoord, ycoord, hit)


def player_move(xcoord, ycoord):
    # This function will check an AI move as a hit or miss, update the AIs board, and then display it on the anvas,
    # given the x and y coordinates for the move, the fat that it is the players turn, and the game is running. If a
    # hit is found, the AIs ships will check their health to see if they've been destroyed.
    import UIControl
    global AI
    if playerTurn and gameRunning:
        hit = False
        if AIBoard[xcoord][ycoord] == "S" or AIBoard[xcoord][ycoord] == "H":  # This checks the board for the outcome.
            hit = True
            AIBoard[xcoord][ycoord] = "H"
            for i in AI.ships:  # This checks all of the AIs ships health.
                i.check_health()
        else:
            AIBoard[xcoord][ycoord] = "M"
        UIControl.board.show_player_move(xcoord, ycoord, hit)


def setup_game():
    # This function initializes the arrays for the player and AI boards.
    global AIBoard, playerBoard
    playerBoard = []
    AIBoard = []
    for i in range(10):  # This creates the AI board
        playerBoard.append([])
        for j in range(10):
            playerBoard[i].append(" ")
    for i in range(10):  # This creates the player board
        AIBoard.append([])
        for j in range(10):
            AIBoard[i].append(" ")


def start_game():
    # This initializes the game as a whole. The AI is generated, and its board is set, and it starts the players turn.
    global difficulty, AI, playerTurn
    import AIControl
    import UIControl
    difficulty = UIControl.difficulty
    AI = AIControl.AI(difficulty)
    AI.gen_board()
    UIControl.board.actionLabel.configure(text="Choose a target:")
    UIControl.board.show_ai_board()
    playerTurn = True
