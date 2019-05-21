# This is the UI Controls. It will also handle player side input
from tkinter import *

# Main UI elements
main = Tk
menu = Frame(main)
howTo = Frame(main)
settings = Frame(main)
playerBoard = Frame(main)
AIBoard = Frame(main)

# Menu UI elements
playButton = Button(menu, text="Play")
howToButton = Button(menu, text="How to Play")
settingsButton = Button(menu, text="Settings")

# How To UI elements
howToText = Text(howTo)
howToText.insert()  # TODO: Insert the how to text here.
howToText.configure(state=DISABLED)

# Settings UI elements
settingsBox = Listbox(settings, selectmode=SINGLE)
settingsBox.insert(1, "Easy")
settingsBox.insert(2, "Normal")
settingsBox.insert(3, "Hard")
settingsBox.see(2)

# Player Board UI elements

