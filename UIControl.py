# This is the UI Controls. It will also handle player side input
from tkinter import *
from PIL import ImageTk, Image

# Difficulty variable
difficulty = None

# Constants
BOARD_OFFSET = 25

# Main UI elements
main = Tk()
main.title("Battleship")
main.geometry("2286x1254")

# Images
backgroundImage = Image.open("Assets/sea image.jpg")  # Width 2286, Height 1254
backgroundImageTK = ImageTk.PhotoImage(backgroundImage)
gridImage = Image.open("Assets/grid.jpg")  # Width 800, Height 800. Rectangles are 8 across, boxes are 89x89
gridImageTK = ImageTk.PhotoImage(gridImage)
shipImg1 = Image.open("Assets/Ship1(5).jpg")
shipImg2 = Image.open("Assets/Ship2(4).jpg")
shipImg3 = Image.open("Assets/Ship3(3).jpg")
shipImg4 = Image.open("Assets/Ship4(4).jpg")
shipImg5 = Image.open("Assets/Ship5(2).jpg")


# Classes
class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.background = Label(self, image=backgroundImageTK)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)


class Menu(MainApplication):
    def __init__(self, parent, *args, **kwargs):
        MainApplication.__init__(self, parent, *args, **kwargs)
        self.buttonHolder = Frame(self)
        self.buttonHolder.place(relx=.5, rely=.45, anchor=CENTER)
        self.playButton = Button(self.buttonHolder, text="Play", command=open_game)
        self.playButton.pack()
        self.howTo = self.MenuElement("How To", main, self)
        self.howTo.text = Text(self.howTo.buttonPack, width=30, height=10)
        self.howTo.text.insert(END,
                               "You and your AI opponent will place ships on a grid and take turns guessing where the "
                               "other player's ships are. When placing a vertical ship, click the ship then click where"
                               " you want the top of the ship to be on the board. When placing a horizontal ship, "
                               "click the ship then click where you want the left end of the ship to be on the board.")
        self.howTo.text.configure(state=DISABLED)
        self.howTo.text.pack()
        self.settings = self.MenuElement("Settings", main, self)
        self.settings.settingsLabel = Label(self.settings.buttonPack, text="Difficulty:")
        self.settings.D1 = Radiobutton(self.settings.buttonPack, text="Easy", variable=difficulty, value=1)
        self.settings.D2 = Radiobutton(self.settings.buttonPack, text="Medium", variable=difficulty, value=2)
        self.settings.D3 = Radiobutton(self.settings.buttonPack, text="Hard", variable=difficulty, value=3)
        self.settings.settingsLabel.pack(side=TOP)
        self.settings.D1.pack(anchor=W, side=TOP)
        self.settings.D2.pack(anchor=W, side=TOP)
        self.settings.D3.pack(anchor=W, side=TOP)
        self.pack(expand=True, fill=BOTH)

    class MenuElement(MainApplication):
        def open(self):
            self.parent.pack_forget()
            self.pack(expand=True, fill=BOTH)

        def close(self):
            self.pack_forget()
            self.parent.pack(expand=True, fill=BOTH)

        def __init__(self, name, root, parent, *args, **kwargs):
            MainApplication.__init__(self, root, *args, **kwargs)
            self.parent = parent
            self.buttonPack = Frame(self)
            self.buttonPack.place(relx=.5, rely=.45, anchor=CENTER)
            self.button = Button(parent.buttonHolder, text=name, command=self.open)
            self.button.pack()
            self.returnButton = Button(self.buttonPack, text="Back", command=self.close)
            self.returnButton.pack(side=BOTTOM)


class GameBoard(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.playerBoard = Canvas(self)
        self.playerBoard.create_image(0, 0, image=gridImageTK, anchor=NW)
        self.AIBoard = self.playerBoard
        self.actionLabel = Label(text="Click on a ship to place:")
        self.actionLabel.pack()
        self.playerBoard.place(x=0, y=BOARD_OFFSET, width=800, height=800)
        self.shipHolder = Frame(self)
        self.shipHolder.place(x=800, y=BOARD_OFFSET)
        self.ships = []
        self.buttons = []
        self.activeShip = None
        self.ships.append(self.ShipCreator(self, 5, shipImg1, 0))
        self.ships.append(self.ShipCreator(self, 4, shipImg2, 0))
        self.ships.append(self.ShipCreator(self, 3, shipImg3, 0))
        self.ships.append(self.ShipCreator(self, 4, shipImg4, 1))
        self.ships.append(self.ShipCreator(self, 2, shipImg5, 1))
        for i in range(10):
            for j in range(10):
                self.buttons.append(self.PlaceButton(self, i + 1, j + 1))

    def show_player_board(self):
        self.AIBoard.place_forget()
        self.playerBoard.place(x=0, y=BOARD_OFFSET, width=800, height=800)

    def show_ai_board(self):
        self.playerBoard.place_forget()
        self.AIBoard.place(x=0, y=BOARD_OFFSET, width=800, height=800)

    class ShipCreator:
        def __init__(self, parent, length, image, direction):
            # Length is the length integer, image an image, direction is 0 for facing up/down, 1 for facing left/right
            self.length = length
            self.imageTk = ImageTk.PhotoImage(image)
            self.parent = parent
            self.direction = direction
            self.button = Button(self.parent.shipHolder, image=self.imageTk, command=self.start_place)
            self.button.pack()

        def start_place(self):
            self.parent.actionLabel.configure(text="Click where you'd like the bottom/left of the ship to be:")
            self.parent.activeShip = self

        def check_place(self, xcoord, ycoord):
            import Main
            can_place = True
            for i in range(self.length + 1):
                if self.direction == 0 and xcoord < 10 and ycoord + i < 10:
                    if Main.playerBoard[xcoord][ycoord + i] != " ":
                        can_place = False
                        break
                elif self.direction == 1 and xcoord + i > 10 and ycoord > 10:
                    if Main.playerBoard[xcoord + i][ycoord] != " ":
                        can_place = False
                        break
                else:
                    can_place = False
                    break
            return can_place

        def place(self, xcoord, ycoord):
            import Main
            if self.check_place(xcoord, ycoord):
                self.parent.playerBoard.create_image(78 * xcoord + 8, 78 * xcoord + 8 + BOARD_OFFSET, image=self.imageTk, anchor=NW)
                for i in range(self.length + 1):
                    if self.direction == 0:
                        Main.playerBoard[xcoord][ycoord + i] = "S"
                    else:
                        Main.playerBoard[xcoord + i][ycoord] = "S"
                self.button.pack_forget()
                del self.button
                self.parent.ships.remove(self)
                if len(self.parent.ships) == 0:
                    for i in self.parent.buttons:
                        i.place_forget()
                    del self.parent.buttons
                    del self.parent.ships
                    # TODO: Start actual game flow here
            else:
                self.parent.activeShip = None
                self.parent.actionLabel.configure(text="Cannot place a ship there!")

    class PlaceButton:
        def __init__(self, parent, xcoord, ycoord):
            global BOARD_OFFSET
            self.xcoord = xcoord
            self.ycoord = ycoord
            self.parent = parent
            self.button = Button(self.parent.playerBoard, image=backgroundImageTK, command=self.place)
            self.button.place(x=78 * xcoord + 8, y=78 * xcoord + 8 + BOARD_OFFSET, anchor=NW, height=78, width=78)

        def place(self):
            if self.parent.activeShip is not None:
                self.parent.activeShip.place(self.xcoord, self.ycoord)


# Menu UI command
def open_game():  # Initializes the game, making the grid buttons for the players ships
    global board
    menu.pack_forget()
    board = GameBoard(main)
    board.pack(expand=True, fill=BOTH)


# Initial setup and game execution functions
def setup_menu():
    global menu
    menu = Menu(main)
    main.mainloop()
