# This is the UI Controls. It will also handle player side input
import main as game
from tkinter import *
from PIL import ImageTk, Image


# Classes
class Ship:
    def __init__(self, length, image, direction):
        # Length is the length integer, image an image, direction is 0 for facing up/down, 1 for facing left/right
        self.length = length
        self.image = image
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.direction = direction

    def check_place(self, xcoord, ycoord):
        can_place = True
        for i in range(self.length + 1):
            if self.direction == 0:
                if game.playerBoard[xcoord][ycoord + i] != " ":
                    can_place = False
                    break
            else:
                if game.playerBoard[xcoord + i][ycoord] != " ":
                    can_place = False
                    break
        return can_place


# Difficulty variable
difficulty = None

# Images
backgroundImage = Image.open("Assets/sea image.jpg")  # Width 2286, Height 1254
backgroundImageTK = ImageTk.PhotoImage(backgroundImage)
gridImage = Image.open("Assets/grid.jpg")  # Width 800, Height 800
gridImageTK = ImageTk.PhotoImage(gridImage)

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
menuBackground = Label(menu, image=backgroundImageTK)
howToBackground = Label(howTo, image=backgroundImageTK)
settingsBackground = Label(settings, image=backgroundImageTK)
gameBackground = Label(board, image=backgroundImageTK)


# Menu UI commands
def open_game():
    menu.pack_forget()
    board.pack(expand=True, fill=BOTH)


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
howToText.insert(END, "You and your AI opponent will place ships on a grid and take turns guessing where the other player's ships are. When placing a vertical ship, click the ship then click where you want the top of the ship to be on the board. When placing a horizontal ship, click the ship then click where you want the left end of the ship to be on the board.")
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
actionLabel = Label(board, text="Place your ships:")
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