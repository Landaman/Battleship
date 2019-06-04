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
menu = Frame(main)
howTo = Frame(main)
settings = Frame(main)
board = Frame(main)

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

# Backgrounds
menuBackground = Label(menu, image=backgroundImageTK)
howToBackground = Label(howTo, image=backgroundImageTK)
settingsBackground = Label(settings, image=backgroundImageTK)
gameBackground = Label(board, image=backgroundImageTK)


# Classes
class ShipCreator:
    global board, BOARD_OFFSET
    ShipHolder = Frame(board)
    ShipHolder.place(x=800, y=BOARD_OFFSET)
    shipNum = 5
    activeShip = None

    def __init__(self, length, image, direction):
        # Length is the length integer, image an image, direction is 0 for facing up/down, 1 for facing left/right
        self.length = length
        self.imageTk = ImageTk.PhotoImage(image)
        self.direction = direction
        self.button = Button(ShipCreator.ShipHolder, image=self.imageTk, command=self.start_place)
        self.button.pack()

    def start_place(self):
        actionLabel.configure(text="Click where you'd like the bottom/left of the ship to be:")
        ShipCreator.activeShip = self

    def check_place(self, xcoord, ycoord):
        import Main
        can_place = True
        for i in range(self.length + 1):
            if self.direction == 0:
                if ycoord + i < 10 and Main.playerBoard[xcoord][ycoord + i] != " ":
                    can_place = False
                    break
            else:
                if xcoord + i < 10 and Main.playerBoard[xcoord + i][ycoord] == " ":
                    can_place = False
                    break
        return can_place

    def place(self, xcoord, ycoord):
        import Main
        global playerBoard
        if self.check_place(xcoord, ycoord):
            playerBoard.create_image(78 * xcoord + 8, 78 * xcoord + 8 + BOARD_OFFSET, image=self.imageTk, anchor=NW)
            for i in range(self.length + 1):
                if self.direction == 0:
                    Main.playerBoard[xcoord][ycoord + i] = "S"
                else:
                    Main.playerBoard[xcoord + i][ycoord] = "S"
            del self.button
            ShipCreator.shipNum -= 1
            if ShipCreator.shipNum == 0:
                for i in range(10):
                    for j in range(10):
                        exec("del button" + str(i) + str(j))
                del ship1, ship2, ship3, ship4, ship5
                # TODO: what the hell else can i do
        else:
            ShipCreator.activeShip = None
            actionLabel.configure(text="Cannot place a ship there!")


class PlaceButton:
    def __init__(self, xcoord, ycoord):
        global BOARD_OFFSET
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.button = Button(playerBoard, image=backgroundImageTK, command=self.place)
        self.button.place(x=78 * xcoord + 8, y=78 * xcoord + 8 + BOARD_OFFSET, anchor=NW, height=78, width=78)

    def place(self):
        if ShipCreator.activeShip is not None:
            ShipCreator.activeShip.place(self.xcoord, self.ycoord)


# Menu UI commands
def open_game():  # Initializes the game, making the grid buttons for the players ships
    global shipImg1, shipImg2, shipImg3, shipImg4, shipImg5, ship1, ship2, ship3, ship4, ship5
    menu.pack_forget()
    board.pack(expand=True, fill=BOTH)
    for i in range(10):
        for j in range(10):
            exec("button" + str(i) + str(j) + " = PlaceButton(" + str(i + 1) + "," + str(j + 1) + ")")
    ship1 = ShipCreator(5, shipImg1, 0)
    ship2 = ShipCreator(4, shipImg2, 0)
    ship3 = ShipCreator(3, shipImg3, 0)
    ship4 = ShipCreator(4, shipImg4, 1)
    ship5 = ShipCreator(5, shipImg5, 1)


def open_how_to():
    menu.pack_forget()
    howTo.pack(expand=True, fill=BOTH)


def open_settings():
    menu.pack_forget()
    settings.pack(expand=True, fill=BOTH)


# Menu UI elements
menuButtons = Label(menu)
playButton = Button(menuButtons, text="Play", command=open_game)
howToButton = Button(menuButtons, text="How to Play", command=open_how_to)
settingsButton = Button(menuButtons, text="Settings", command=open_settings)
menuBackground.place(x=0, y=0, relwidth=1, relheight=1)
playButton.pack()
howToButton.pack()
menuButtons.place(anchor=CENTER, relx=.5, rely=.45)
settingsButton.pack()


# How To UI commands
def how_to_return():
    howTo.pack_forget()
    menu.pack(expand=True, fill=BOTH)


# How To UI elements
howToElements = Frame(howTo)
howToText = Text(howToElements, width=30, height=10)
howToText.insert(END, "You and your AI opponent will place ships on a grid and take turns guessing where the other "
                      "player's ships are. When placing a vertical ship, click the ship then click where you want the "
                      "top of the ship to be on the board. When placing a horizontal ship, click the ship "
                      "then click where you want the left end of the ship to be on the board.")
howToText.configure(state=DISABLED)
howToReturn = Button(howToElements, text="Back", command=how_to_return)
howToBackground.place(x=0, y=0, relwidth=1, relheight=1)
howToText.pack(side=TOP)
howToElements.place(anchor=CENTER, relx=.5, rely=.45)
howToReturn.pack(side=TOP)


# Settings UI commands
def settings_return():
    settings.pack_forget()
    menu.pack(expand=True, fill=BOTH)


# Settings UI elements
optionsArea = Frame(settings)
settingsLabel = Label(optionsArea, text="Difficulty:")
D1 = Radiobutton(optionsArea, text="Easy", variable=difficulty, value=1)
D2 = Radiobutton(optionsArea, text="Medium", variable=difficulty, value=2)
D3 = Radiobutton(optionsArea, text="Hard", variable=difficulty, value=3)
settingsReturn = Button(optionsArea, text="Back", command=settings_return)
settingsBackground.place(x=0, y=0, relwidth=1, relheight=1)
settingsLabel.pack(side=TOP)
D1.pack(anchor=W, side=TOP)
D2.pack(anchor=W, side=TOP)
D3.pack(anchor=W, side=TOP)
optionsArea.place(anchor=CENTER, relx=.5, rely=.45)
settingsReturn.pack(side=TOP)

# Game board UI elements
actionLabel = Label(board, text="Click on a ship to place:")
playerBoard = Canvas(board)
playerBoard.create_image(0, 0, image=gridImageTK, anchor=NW)  # The image is 800x800
AIBoard = playerBoard
actionLabel.pack()
playerBoard.place(x=0, y=BOARD_OFFSET, width=800, height=800)


# Initial setup and game execution functions
def setup_menu():
    menuBackground.place(x=0, y=0, relwidth=1, relheight=1)
    menu.pack(expand=True, fill=BOTH)
    main.mainloop()
