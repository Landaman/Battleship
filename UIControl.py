# This is the UI Controls. It will also handle player side input
import tkinter as tk
from PIL import ImageTk, Image

# Global variables
difficulty = None
menu = None
board = None
victory = None

# Board constants
BOARD_OFFSET = 36
BOARD_WIDTH = 978
BOARD_HEIGHT = 978
BOX_OFFSET = 8
BOX_WIDTH = 89
BOX_HEIGHT = 89

# Main UI elements
main = tk.Tk()
main.title("Battleship")
main.geometry("2286x1254")

# Images
buttonBackgroundImage = Image.open("Assets/button background.jpg")
backgroundImage = Image.open("Assets/sea image.jpg")
gridImage = Image.open("Assets/grid.jpg")
shipImg1 = Image.open("Assets/Ship1(4).jpg")
shipImg2 = Image.open("Assets/Ship2(4).jpg")
shipImg3 = Image.open("Assets/Ship3(3).jpg")
shipImg4 = Image.open("Assets/Ship4(4).jpg")
shipImg5 = Image.open("Assets/Ship5(2).jpg")
missImage = Image.open("Assets/miss.jpg")
hitImage = Image.open("Assets/hit.jpg")


# Classes
class MainButton(tk.Button):
    # This is a button class. It is designed to be used as a template for other classes being placed on the board. In
    # this state, it has the ability to place itself on the board, and clean itself up.
    def __init__(self, parent_array, parent_board, xcoord, ycoord, *args, **kwargs):
        # parent_array is the array that the buttons are being stored in, parent_board is the board that the buttons
        # are on, xcoord is the x coordinate of the button, and ycoord is the y coordinate of the button.
        tk.Button.__init__(self, parent_board, *args, **kwargs)
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.parentArray = parent_array
        self.parentBoard = parent_board
        self.backgroundImageTk = ImageTk.PhotoImage(buttonBackgroundImage)
        self.configure(image=self.backgroundImageTk)
        self.place(x=BOX_WIDTH * self.xcoord + ((self.xcoord + 1) * BOX_OFFSET), y=BOX_HEIGHT * self.ycoord +
                                               ((self.ycoord + 1) * BOX_OFFSET),
                   height=BOX_WIDTH + BOX_OFFSET, width=BOX_HEIGHT + BOX_OFFSET, anchor=tk.NW)

    def cleanup(self):
        # This removes the button from the board.
        self.place_forget()


class MainApplication(tk.Frame):
    # This is a screen template. It generates a screen with a background.
    def __init__(self, parent, *args, **kwargs):
        # Parent is the parent of the screen, usually the root. *args and **kwargs are any other arguments.
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.backgroundImageTk = ImageTk.PhotoImage(backgroundImage)
        self.background = tk.Label(self, image=self.backgroundImageTk)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)


class Victory(MainApplication):
    # This is the victory screen. It is a MainApplication, meaning it has a background, and it displays
    # who won with the option to quit.
    def __init__(self, winner, parent, *args, **kwargs):
        # parent, *args, and **kwargs are the same as in MainApplication.
        MainApplication.__init__(self, parent, *args, **kwargs)
        self.victoryLabel = tk.Label(self, text=winner + " won!")
        self.victoryLabel.place(relx=.5, rely=.45, anchor=tk.CENTER)
        self.quit = tk.Button(self, text="Quit", command=self.quit)
        self.quit.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.pack(expand=True, fill=tk.BOTH)

    def quit(self):
        # This is the callback for the button. It simply quits the program.
        main.quit()


class Menu(MainApplication):
    # This is the menu application. It generates 3 different options: Play, which starts the game, How To which
    # explains how to play, and finally Settings, which allows the user to adjust the difficulty.
    def __init__(self, parent, *args, **kwargs):
        # All options are the same as in the parent MainApplication.
        MainApplication.__init__(self, parent, *args, **kwargs)
        # This generates the menu screen and the options.
        self.buttonHolder = tk.Frame(self)
        self.buttonHolder.place(relx=.5, rely=.45, anchor=tk.CENTER)
        self.label = tk.Label(self.buttonHolder, text="Battleship:")
        self.label.pack()
        self.playButton = tk.Button(self.buttonHolder, text="Play", command=open_game)
        self.playButton.pack()
        self.howTo = self.MenuElement("How To", main, self)
        self.howTo.text = tk.Text(self.howTo.buttonPack, width=30, height=15)
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
        # The menu screen is automatically packed.
        self.pack(expand=True, fill=tk.BOTH)

    class MenuElement(MainApplication):
        # The MenuElement class is for the Settings and How To windows. It's a frame, but it contains a button within
        # the frame, an organizer for menu elements, and a button in the menu to enter the frame.
        def __init__(self, name, root, parent, *args, **kwargs):
            # Name is the name displayed on the button, parent is the menu, and root is the main application so that
            # the frame can be displayed in it. All other options are the same as MainApplication.
            MainApplication.__init__(self, root, *args, **kwargs)
            self.parent = parent
            # This sets up the two buttons and organizer described above.
            self.buttonPack = tk.Frame(self)
            self.buttonPack.place(relx=.5, rely=.45, anchor=tk.CENTER)
            self.button = tk.Button(parent.buttonHolder, text=name, command=self.open)
            self.button.pack()
            self.returnButton = tk.Button(self.buttonPack, text="Back", command=self.close)
            self.returnButton.pack(side=tk.BOTTOM)

        def open(self):
            # This opens the MenuElement. It is the callback for the open button present in the parent.
            self.parent.pack_forget()
            self.pack(expand=True, fill=tk.BOTH)

        def close(self):
            # This returns to the parent menu. It is the callback for the button present in the frame.
            self.pack_forget()
            self.parent.pack(expand=True, fill=tk.BOTH)


class GameBoard(tk.Frame):
    import Game
    # This is the GameBoard itself. It stores the canvases, ships, buttons, and all other UI elements that go into
    # playing the game. It will automatically set itself up to be ready to place player ships, and when that's done
    # it will call back to the Game library and start the game.

    def __init__(self, parent, *args, **kwargs):
        # Parent is the root for the board to be displayed on, *args and **kwargs are any other options for the screen.
        import Game
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.playerBoardCanvas = tk.Canvas(self)
        # These are the UI elements for the menu
        self.gridImageTk = ImageTk.PhotoImage(gridImage)
        self.missImageTk = ImageTk.PhotoImage(missImage)
        self.hitImageTk = ImageTk.PhotoImage(hitImage)
        self.playerBoardCanvas.create_image(0, 0, image=self.gridImageTk, anchor=tk.NW)
        self.AIBoardCanvas = tk.Canvas(self)
        self.AIBoardCanvas.create_image(0, 0, image=self.gridImageTk, anchor=tk.NW)
        self.actionLabel = tk.Label(self, text="Click on a ship to place:")
        self.actionLabel.pack()
        self.playerBoardCanvas.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.shipHolder = tk.Frame(self)
        self.shipHolder.place(x=1000, y=BOARD_OFFSET)
        # These are the storage arrays for the menu
        self.placeButtons = []
        self.playerShips = []
        self.moveButtons = []
        # These are the variables for the menu
        self.activePlaceShip = None
        self.toBePlaced = 5
        self.parent = parent
        self.proceedButton = None
        # These are the players ships.
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoardCanvas, 4, 0,
                                                 shipImg1))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoardCanvas, 4, 0,
                                                 shipImg2))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoardCanvas, 3, 0,
                                                 shipImg3))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoardCanvas, 4, 1,
                                                 shipImg4))
        self.playerShips.append(self.ShipCreator(self, self.playerShips, Game.playerBoard, self.playerBoardCanvas, 2, 1,
                                                 shipImg5))
        for i in range(10): # This sets up the buttons on the board for placing the players ships.
            for j in range(10):
                self.placeButtons.append(self.PlaceButton(self, i, j))

    def show_player_board(self):
        # This hides the AI board and shows the player board. Meant for use during the game.
        self.AIBoardCanvas.place_forget()
        self.playerBoardCanvas.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)

    def show_ai_board(self):
        # This hides the player board and shows the AI board. Meant for use during the game.
        self.playerBoardCanvas.place_forget()
        self.AIBoardCanvas.place(x=0, y=BOARD_OFFSET, width=BOARD_WIDTH, height=BOARD_HEIGHT)

    def setup_buttons(self):
        # This sets up the board buttons for use during game play.
        for i in range(10): # This generates one for each square.
            for j in range(10):
                self.moveButtons.append(self.MoveButton(self, i, j))
        # This is a button that allows the player to get back to their own turn after seeing the AI turn
        self.proceedButton = tk.Button(self, text="Continue", command=self.finish_wait, font=("arial", 30))

    def show_ai_move(self, xcoord, ycoord, hit):
        # This shows the AIs move. Meant for use during the game.
        if hit:  # This creates a marker to show whether the AI hit or missed
            self.playerBoardCanvas.create_image(xcoord * BOX_WIDTH + ((xcoord + 1) * BOX_OFFSET),
                                                ycoord * BOX_HEIGHT + ((ycoord + 1) * BOX_OFFSET),
                                                image=self.hitImageTk, anchor=tk.NW)
        else:
            self.playerBoardCanvas.create_image(xcoord * BOX_WIDTH + ((xcoord + 1) * BOX_OFFSET),
                                                ycoord * BOX_HEIGHT + ((ycoord + 1) * BOX_OFFSET),
                                                image=self.missImageTk, anchor=tk.NW)
        # This reconfigures the label to tell the player what is happening, packs the proceed button and shows
        # the player board.
        self.actionLabel.configure(text="AI Move:")
        self.proceedButton.place(relx=.75, rely=.5, anchor=tk.CENTER)
        self.show_player_board()

    def show_player_move(self, xcoord, ycoord, hit):
        # This shows the players move. Meant for use during the game.
        import Game
        if hit:  # This displays a marker showing whether the move was a hit or miss.
            self.AIBoardCanvas.create_image(xcoord * BOX_WIDTH + ((xcoord + 1) * BOX_OFFSET),
                                            ycoord * BOX_HEIGHT + ((ycoord + 1) * BOX_OFFSET),
                                            image=self.hitImageTk, anchor=tk.NW)
        else:
            self.AIBoardCanvas.create_image(xcoord * BOX_WIDTH + ((xcoord + 1) * BOX_OFFSET),
                                            ycoord * BOX_HEIGHT + ((ycoord + 1) * BOX_OFFSET),
                                            image=self.missImageTk, anchor=tk.NW)
        # This ends the players turn and starts the AIs move generation.
        Game.playerTurn = False
        Game.AI.get_hit()

    def finish_wait(self):
        # This is the callback for the continue button to end the AIs turn. It repacks the players screen,
        # updates the label and starts the players turn.
        import Game
        self.proceedButton.place_forget()
        self.actionLabel.configure(text="Choose a target:")
        self.show_ai_board()
        Game.playerTurn = True

    class ShipCreator(Game.Ship):
        # This class is meant for creating the players ships as the game goes on. In inherits from the Game.Ship class.
        def __init__(self, parent, parent_container, parent_board, parent_canvas, length, direction, image):
            # Everything except for parent are the same as the parent Game.Ship class. Parent is the Frame that the
            # game is being played in, I.E. the game board.
            import Game
            Game.Ship.__init__(self, parent_container, parent_board, parent_canvas, length, direction, image)
            # This sets up the button to show where the ship is before the game has started and the button to allow
            # the process to start.
            self.parent = parent
            self.button = tk.Button(self.parent.shipHolder, image=self.imageTk, command=self.start_place)
            self.button.pack()
            self.image = tk.Label(self.parent, image=self.imageTk)

        def start_place(self):
            # This is the callback for the button to allow the process to start. It designates an active ship, and then
            # updates the action label.
            self.parent.actionLabel.configure(text="Click where you'd like the bottom/left of the ship to be:")
            self.parent.activePlaceShip = self

        def place(self, xcoord, ycoord):
            # This final placement process. Is places the ship on the board, and a temporary label,
            # then checks to see if more ships need to be placed, and if not it preps the board for game play.
            import Game
            if self.check_place(xcoord, ycoord):  # Checks the placement
                self.board_place(xcoord, ycoord)
                # Puts a temporary image down so that you can see where the ship is over the buttons.
                self.image.place(x=BOX_WIDTH * self.xcoord + ((self.xcoord + 1) * BOX_OFFSET),
                                 y=BOX_HEIGHT * self.ycoord + ((self.ycoord + 1) * BOX_OFFSET) + BOARD_OFFSET,
                                 anchor=tk.NW)
                # This unpacks the initial ship button.
                self.button.pack_forget()
                # This updates the toBePlaced variable to indicate a ship has been placed.
                self.parent.toBePlaced -= 1
                # This updates the action label.
                self.parent.activePlaceShip = None
                self.parent.actionLabel.configure(text="Click on a ship to place:")
                if self.parent.toBePlaced == 0:  # Checks if all player ships have been placed.
                    for i in self.parent.placeButtons:  # This cleans up the placement buttons.
                        i.cleanup()
                    for i in self.parent.playerShips:  # This cleans up all of the ships, removing the temporary image.
                        i.cleanup()
                    del self.parent.placeButtons
                    del self.parent.toBePlaced
                    self.parent.setup_buttons()
                    Game.start_game()
            else:
                self.parent.activePlaceShip = None
                self.parent.actionLabel.configure(text="Cannot place a ship there!")

        def cleanup(self):
            # This cleans up the ship by removing the temporary image.
            self.image.place_forget()

    class PlaceButton(MainButton):
        # These are put down on the board during the ship placement process. When one is clicked, its coordinates
        # are passed to the active ship to attempt a placement.
        def __init__(self, parent, xcoord, ycoord):
            # Parent is the game board. xcoord and ycoord are the x and y coordinates of where the button is.
            MainButton.__init__(self, parent.placeButtons, parent.playerBoardCanvas, xcoord, ycoord)
            self.parent = parent
            self.configure(command=self.place_ship)

        def place_ship(self):
            # This is the placement process. If there is an active ship, the coordinates of this button are passed to
            # it. This is the callback for the button/class.
            if self.parent.activePlaceShip is not None:
                self.parent.activePlaceShip.place(self.xcoord, self.ycoord)

    class MoveButton(MainButton):
        # This is the move button. These are placed on the AIs board to allow the player to attempt moves.
        def __init__(self, parent, xcoord, ycoord):
            # Parent is the game board, xcoord and ycoord are the x and y coordinates of the button.
            MainButton.__init__(self, parent.moveButtons, parent.AIBoardCanvas, xcoord, ycoord)
            self.parent = parent
            self.configure(command=self.player_move)

        def player_move(self):
            # This is the callback for the button/class. It passes the buttons position to the player move function and
            # then the button deletes itself.
            import Game
            self.cleanup()
            Game.player_move(self.xcoord, self.ycoord)


# Game initializer
def open_game():  # Initializes the game, making the grid buttons for the players ships
    global board
    menu.pack_forget()
    board.pack(expand=True, fill=tk.BOTH)


# Initial setup and game execution functions
def setup_menu():
    # This sets up the menu, and the game board to improve loading times once execution has started. First thing to be
    # run.
    import Game
    global menu, main, board
    main.option_add("*Font", "arial 21")
    Game.setup_game()
    board = GameBoard(main)
    menu = Menu(main)
    main.mainloop()


def setup_victory(winner):
    # This shows the victory screen, victory is a string of the victor.
    global victory, main
    board.pack_forget()
    victory = Victory(winner, main)
