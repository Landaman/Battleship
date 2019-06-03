# This is the general program flow and game execution
import UIControl
UIControl.setup_menu()

# Game setup
BASE_BOARD = []
for i in range(10):  # This creates the stock board
    BASE_BOARD.append([])
    for j in range(10):
        BASE_BOARD[i].append(" ")
AIBoard = BASE_BOARD
playerBoard = BASE_BOARD

#player turn is set up on a system that checks if a coord has a ship on it (ship on coord -> "full")
def pturn(){
ptarget = input("Select where on the grid you would like to fire.")
    if ptarget = full{
        #(show hit marker on coordinate)
        print("You hit a ship!")
    }
    else{
        #(show miss marker on coordinate)
        print("You missed.")
    }
    aiturn()
    }
