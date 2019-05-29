# This is the UI Controls. It will also handle player side input
from tkinter import *
from PIL import ImageTk, Image

# Difficulty variable
difficulty = None

# Main UI elements
main = Tk()
main.title("Battleship")
main.geometry("2286x1254")
backgroundImage = Image.open("Assets/sea image.jpg")  # Width 2286, Height 1254
backgroundImageTK = ImageTk.PhotoImage(backgroundImage)
menu = Frame(main)
howTo = Frame(main)
settings = Frame(main)
board = Frame(main)
menuBackground = Label(menu, image=backgroundImageTK)
howToBackground = Label(howTo, image=backgroundImageTK)
settingsBackground = Label(howTo, image=backgroundImageTK)
gameBackground = Label(board, image=backgroundImageTK)


# Menu UI commands
def open_game():
    menu.pack_forget()
    board.pack()


def open_how_to():
    menu.pack_forget()
    howTo.pack()


def open_settings():
    menu.pack_forget()
    settings.pack()


# Menu UI elements
playButton = Button(menu, text="Play", command=open_game)
howToButton = Button(menu, text="How to Play", command=open_how_to)
settingsButton = Button(menu, text="Settings", command=open_settings)
menuBackground.place(x=0, y=0, relwidth=1, relheight=1)
playButton.pack()
howToButton.pack()
settingsButton.pack()


# How To UI commands
def how_to_return():
    howTo.pack_forget()
    menu.pack()


# How To UI elements
howToText = Text(howTo, width=30, height=10)
howToText.insert(END, "You and your AI opponent will place ships on a grid and take turns guessing where the other player's ships are. When placing a vertical ship, click the ship then click where you want the top of the ship to be on the board. When placing a horizontal ship, click the ship then click where you want the left end of the ship to be on the board.")  # TODO: Insert the how to text here
howToText.configure(state=DISABLED)
howToReturn = Button(howTo, text="Back", command=how_to_return)
howToBackground.place(x=0, y=0, relwidth=1, relheight=1)
howToText.pack(side=TOP)
howToReturn.pack(side=TOP)


# Settings UI commands
def settings_return():
    settings.pack_forget()
    menu.pack()


# Settings UI elements
settingsLabel = Label(settings, text="Difficulty:")
D1 = Radiobutton(settings, text="Easy", variable=difficulty, value=1)
D2 = Radiobutton(settings, text="Medium", variable=difficulty, value=2)
D3 = Radiobutton(settings, text="Hard", variable=difficulty, value=3)
settingsReturn = Button(settings, text="Back", command=settings_return)
settingsBackground.place(x=0, y=0, relwidth=1, relheight=1)
settingsLabel.pack(side=TOP)
D1.pack(anchor=W, side=TOP)
D2.pack(anchor=W, side=TOP)
D3.pack(anchor=W, side=TOP)
settingsReturn.pack(side=TOP)


# Initial setup
def setup_menu():
    menuBackground.place(x=0, y=0, relwidth=1, relheight=1)
    menu.pack()
    main.mainloop()


# TODO: Transparent UI elements
# TODO: Make the background fill the full  image
