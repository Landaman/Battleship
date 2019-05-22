# This is the UI Controls. It will also handle player side input
from tkinter import *

# Difficulty variable
difficulty = None

# Main UI elements
main = Tk()
window = LabelFrame(main)
menu = Frame(window)
howTo = Frame(window)
settings = Frame(window)
board = PanedWindow(window)


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
playButton.pack()
howToButton.pack()
settingsButton.pack()


# How To UI commands
def how_to_return():
    howTo.pack_forget()
    menu.pack()


# How To UI elements
howToText = Text(howTo)
howToText.insert(END, "Placeholder")  # TODO: Insert the how to text here
howToText.configure(state=DISABLED)
howToReturn = Button(howTo, text="Back", command=how_to_return)
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
settingsLabel.pack(side=TOP)
D1.pack(anchor=W, side=TOP)
D2.pack(anchor=W,side=TOP)
D3.pack(anchor=W,side=TOP)
settingsReturn.pack(side=TOP)


# Initial setup
def setup_menu():
    menu.pack()
    window.pack()
    main.mainloop()
