# This is the UI Controls. It will also handle player side input
import tkinter as tk
from PIL import ImageTk, Image

# Global variables
difficulty = None
menu = None
board = None
victory = None

# Constants
BOARD_OFFSET = 25
BOARD_WIDTH = 996
BOARD_HEIGHT = 992
BOX_OFFSET = 8
BOX_WIDTH = 97
BOX_HEIGHT = 97

# Main UI elements
main = tk.Tk()
main.title("Battleship")
main.geometry("2286x1254")

# Images
backgroundImage = Image.open("Assets/sea image.jpg")  # Width 2286, Height 1254
gridImage = Image.open("Assets/grid.jpg")  # Width 800, Height 800. Rectangles are 8 across, boxes are 89x89
shipImg1 = Image.open("Assets/Ship1(5).jpg")
shipImg2 = Image.open("Assets/Ship2(4).jpg")
shipImg3 = Image.open("Assets/Ship3(3).jpg")
shipImg4 = Image.open("Assets/Ship4(4).jpg")
shipImg5 = Image.open("Assets/Ship5(2).jpg")
missImage = Image.open("Assets/miss.jpg")
hitImage = Image.open("Assets/hit.jpg")


# Classes
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.backgroundImageTk = ImageTk.PhotoImage(backgroundImage)
        self.background = tk.Label(self, image=self.backgroundImageTk)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)


class Victory(MainApplication):
    def __init__(self, winner, parent, *args, **kwargs):
        MainApplication.__init__(self, parent, *args, **kwargs)
        self.victoryLabel = tk.Label(self, text=winner + " won!")
        self.victoryLabel.place(relx=.5, rely=.45, anchor=tk.CENTER)
        self.quit = tk.Button(self, text="Quit", command=self.quit)
        self.quit.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.pack(expand=True, fill=tk.BOTH)

    def quit(self):
        main.quit()


class Menu(MainApplication):
    def __init__(self, parent, *args, **kwargs):
        MainApplication.__init__(self, parent, *args, **kwargs)
        self.buttonHolder = tk.Frame(self)
        self.buttonHolder.place(relx=.5, rely=.45, anchor=tk.CENTER)
        self.playButton = tk.Button(self.buttonHolder, text="Play", command=open_game)
        self.playButton.pack()
        self.howTo = self.MenuElement("How To", main, self)
        self.howTo.text = tk.Text(self.howTo.buttonPack, width=30, height=10)
        self.howTo.text.insert(tk.END,
                               "You and your AI opponent will place ships on a grid and take turns guessing where the "
                               "other player's ships are. When placing a vertical ship, click the ship then click where"
                               " you want the top of the ship to be on the board. When placing a horizontal ship, "
                               "click the ship then click where you want the left end of the ship to be on the board.")
        self.howTo.text.configure(state=tk.DISABLED)
        self.howTo.text.pack()
        self.settings = self.MenuElement("Settings", main, self)
        self.settings.settingsLabel = tk.Label(self.settings.buttonPack, text="Difficulty:")
        self.settings.D1 = tk.Radiobutton(self.settings.buttonPack, text="Easy", variable=difficulty, value=1)
        self.settings.D2 = tk.Radiobutton(self.settings.buttonPack, text="Medium", variable=difficulty, value=2)
        self.settings.D3 = tk.Radiobutton(self.settings.buttonPack, text="Hard", variable=difficulty, value=3)
        self.settings.settingsLabel.pack(side=tk.TOP)
        self.settings.D1.pack(anchor=tk.W, side=tk.TOP)
        self.settings.D2.pack(anchor=tk.W, side=tk.TOP)
        self.settings.D3.pack(anchor=tk.W, side=tk.TOP)
        self.pack(expand=True, fill=tk.BOTH)

    class MenuElement(MainApplication):
        def open(self):
            self.parent.pack_forget()
            self.pack(expand=True, fill=tk.BOTH)

        def close(self):
            self.pack_forget()
            self.parent.pack(expand=True, fill=tk.BOTH)

        def __init__(self, name, root, parent, *args, **kwargs):
            MainApplication.__init__(self, root, *args, **kwargs)
            self.parent = parent
            self.buttonPack = tk.Frame(self)
            self.buttonPack.place(relx=.5, rely=.45, anchor=tk.CENTER)
            self.button = tk.Button(parent.buttonHolder, text=name, command=self.open)
            self.button.pack()
            self.returnButton = tk.Button(self.buttonPack, text="Back", command=self.close)
            self.returnButton.pack(side=tk.BOTTOM)


class GameBoard(tk.Frame):
    import Game

    def __init__(self, parent, *args, **kwargs):
        import Game
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.playerBoard = tk.Canvas(self)
        self.gridImageTk = ImageTk.PhotoImage(gridImage)
        self.missImageTk = ImageTk.PhotoImage(missImage)
        self.hitImageTk = ImageTk.PhotoImage(hitImage)
        self.playerBoard.create_image(0, 0, image=self.gridImageTk, anchor=tk.NW)
        self.AIBoard = tk.Canvas(self)
        self.AIBoard.create_image(0, 0, image=self.gridImageTk, anchor=tk.NW)
        self.actionLabel = tk.Label(text="Click on a ship to place:")
        self.actionLabel.pack()
        self.playerBoard.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.shipHolder = tk.Frame(self)
        self.shipHolder.place(x=1000, y=BOARD_OFFSET)
        self.buttons = []
        self.playerShips = []
        self.AIShips = []
        self.moveButtons = []
        self.activeShip = None
        self.toBePlaced = 5
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoard, 5, 0,
                                                 shipImg1))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoard, 4, 0,
                                                 shipImg2))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoard, 3, 0,
                                                 shipImg3))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoard, 4, 1,
                                                 shipImg4))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoard, 2, 1,
                                                 shipImg5))
        for i in range(10):
            for j in range(10):
                self.buttons.append(self.PlaceButton(self, i, j))

    def show_player_board(self):
        self.AIBoard.place_forget()
        self.playerBoard.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)

    def show_ai_board(self):
        self.playerBoard.place_forget()
        self.AIBoard.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)

    def setup_buttons(self):
        for i in range(10):
            for j in range(10):
                self.moveButtons.append(self.MoveButton(self.AIBoard, i, j))

    def show_ai_move(self, xcoord, ycoord, hit):
        import time
        import Game
        if hit:
            self.playerBoard.create_image(xcoord * BOX_WIDTH + BOX_OFFSET, ycoord * BOX_HEIGHT + BOX_OFFSET,
                                          image=self.hitImageTk, anchor=tk.NW)
        else:
            self.playerBoard.create_image(xcoord * BOX_WIDTH + BOX_OFFSET, ycoord * BOX_HEIGHT + BOX_OFFSET,
                                          image=self.missImageTk, anchor=tk.NW)
        self.show_player_board()
        #time.sleep(45) TODO: Find an alternative to this
        self.show_ai_board()
        Game.playerTurn = True

    def show_player_move(self, xcoord, ycoord, hit):
        import time
        import Game
        if hit:
            self.AIBoard.create_image(xcoord * BOX_WIDTH + BOX_OFFSET, ycoord * BOX_HEIGHT + BOX_OFFSET,
                                      image=self.hitImageTk, anchor=tk.NW)
        else:
            self.AIBoard.create_image(xcoord * BOX_WIDTH + BOX_OFFSET, ycoord * BOX_HEIGHT + BOX_OFFSET,
                                      image=self.missImageTk, anchor=tk.NW)
        #time.sleep(45) TODO: Find an alternative to this
        Game.playerTurn = False
        Game.AI.get_hit()

    class ShipCreator(Game.Ship):
        def __init__(self, parent, parent_container, parent_board, parent_canvas, length, direction, image):
            import Game
            Game.Ship.__init__(self, parent_container, parent_board, parent_canvas, length, direction, image)
            self.parent = parent
            self.button = tk.Button(self.parent.shipHolder, image=self.imageTk, command=self.start_place)
            self.button.pack()
            self.image = tk.Label(self.parent, image=self.imageTk)

        def start_place(self):
            self.parent.actionLabel.configure(text="Click where you'd like the bottom/left of the ship to be:")
            self.parent.activeShip = self

        def place(self, xcoord, ycoord):
            import Game
            if self.check_place(xcoord, ycoord):
                self.board_place(xcoord, ycoord)
                self.image.place(x=BOX_WIDTH * xcoord + BOX_OFFSET, y=BOX_HEIGHT * ycoord + BOX_OFFSET + BOARD_OFFSET)
                self.button.pack_forget()
                self.parent.toBePlaced -= 1
                self.parent.activeShip = None
                if self.parent.toBePlaced == 0:
                    for i in self.parent.buttons:
                        i.cleanup()
                    for i in self.parent.playerShips:
                        i.cleanup()
                    del self.parent.buttons
                    del self.parent.toBePlaced
                    self.parent.setup_buttons()
                    Game.start_game()
            else:
                self.parent.activeShip = None
                self.parent.actionLabel.configure(text="Cannot place a ship there!")

        def cleanup(self):
            self.image.place_forget()

    class PlaceButton:
        def __init__(self, parent, xcoord, ycoord):
            global BOARD_OFFSET
            self.xcoord = xcoord
            self.ycoord = ycoord
            self.parent = parent
            self.backgroundImageTk = ImageTk.PhotoImage(backgroundImage)
            self.button = tk.Button(self.parent.playerBoard, image=self.backgroundImageTk, command=self.place)
            self.button.place(x=BOX_WIDTH * self.xcoord + BOX_OFFSET, y=BOX_HEIGHT * self.ycoord + BOX_OFFSET,
                              anchor=tk.NW, height=BOX_WIDTH, width=BOX_HEIGHT)

        def place(self):
            if self.parent.activeShip is not None:
                self.parent.activeShip.place(self.xcoord, self.ycoord)

        def cleanup(self):
            self.button.place_forget()

    class MoveButton:
        def __init__(self, parent, xcoord, ycoord):
            self.xcoord = xcoord
            self.ycoord = ycoord
            self.parent = parent
            self.backgroundImageTk = ImageTk.PhotoImage(backgroundImage)
            self.button = tk.Button(self.parent, image=self.backgroundImageTk, command=self.player_move)
            self.button.place(x=self.xcoord * BOX_WIDTH + BOX_OFFSET, y=self.ycoord * BOX_HEIGHT + BOX_OFFSET,
                              width=BOX_WIDTH, height=BOX_HEIGHT)

        def player_move(self):
            import Game
            self.button.place_forget()
            Game.player_move(self.xcoord, self.ycoord)


# Game initializer
def open_game():  # Initializes the game, making the grid buttons for the players ships
    global board
    menu.pack_forget()
    board = GameBoard(main)
    board.pack(expand=True, fill=tk.BOTH)


# Initial setup and game execution functions
def setup_menu():
    import Game
    global menu
    Game.setup_game()
    menu = Menu(main)
    main.mainloop()


def setup_victory(winner):
    global victory
    board.pack_forget()
    victory = Victory(main, winner)
