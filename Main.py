# This is the general program flow and game execution
import UIControl

# Game setup
BASE_BOARD = []
for i in range(10):  # This creates the stock board
    BASE_BOARD.append([])
    for j in range(10):
        BASE_BOARD[i].append(" ")
AIBoard = BASE_BOARD
playerBoard = BASE_BOARD

UIControl.setup_menu()
