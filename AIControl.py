# This is the AI Control, both board setup and actual moves
class AI:
    # This is the AI class. Given difficulty it will, generate all of its ships, and then place them using the
    # Game.Ship class. It can then semi-intelligently generate generate moves.
    def __init__(self, difficulty):
        # Difficulty is the difficulty, passed through the Game library from the UI.
        import Game
        import UIControl
        self.difficulty = difficulty
        # Ships are generated and placed in an array.
        self.ships = []
        self.ships.append(Game.Ship(self.ships, Game.AIBoard, UIControl.board.AIBoardCanvas, 5, 0,
                                    UIControl.shipImg1))
        self.ships.append(Game.Ship(self.ships, Game.AIBoard, UIControl.board.AIBoardCanvas, 4, 0,
                                    UIControl.shipImg2))
        self.ships.append(Game.Ship(self.ships, Game.AIBoard, UIControl.board.AIBoardCanvas, 3, 0,
                                    UIControl.shipImg3))
        self.ships.append(Game.Ship(self.ships, Game.AIBoard, UIControl.board.AIBoardCanvas, 4, 1,
                                    UIControl.shipImg4))
        self.ships.append(Game.Ship(self.ships, Game.AIBoard, UIControl.board.AIBoardCanvas, 2, 1,
                                    UIControl.shipImg5))

    def gen_board(self):
        # This randomly generates a the ship placement, with ships closer to the center as the difficulty increases.
        import random
        for i in range(len(self.ships)):  # Every ship is placed
            while True:  # It's looped so that placements can be ensured to be valid.
                if self.difficulty == 1:  # Difficulty check
                    randx = random.randint(0, 9)
                    randy = random.randint(0, 9)
                elif self.difficulty == 2:
                    randx = random.randint(1, 8)
                    randy = random.randint(1, 8)
                else:
                    randx = random.randint(2, 7)
                    randy = random.randint(2, 7)
                if self.ships[i].check_place(randx, randy):  # This checks if the placement is valid. If so, break.
                    self.ships[i].board_place(randx, randy)
                    break

    def get_hit(self):
        # This will somewhat randomly generate a move based on the difficulty.
        import random
        import Game
        if self.difficulty == 1:
            # If the difficulty is one, the move will be completely random.
            while True:  # Checking to make sure we're not firing on something we've already hit or missed
                randx = random.randint(0, 9)
                randy = random.randint(0, 9)
                if Game.playerBoard[randx][randy] == "S" or Game.playerBoard[randx][randy] == " ":
                    Game.ai_move(randx, randy)
                    break
        else:
            # It's random unless there's a hit. If there's a hit, it will try and shoot around that hit, trying each
            # possible side for another hit. If it's tried that and can't get any more hits, it will move on to
            # another random target.
            has_hit = False
            for i in range(10):  # This scans the board for hits.
                for j in range(10):
                    if Game.playerBoard[i][j] == "H":
                        if i > 0:
                            if Game.playerBoard[i - 1][j] == "S" or Game.playerBoard[i - 1][j] == " ":
                                # This checks to see if it can fire to the right of the target.
                                Game.ai_move(i - 1, j)
                                has_hit = True
                                break
                        elif i < 10:
                            if Game.playerBoard[i + 1][j] == "S" or Game.playerBoard[i + 1][j] == " ":
                                # This checks to see if it can fire to the left of the target.
                                Game.ai_move(i + 1, j)
                                has_hit = True
                                break
                        elif j > 0:
                            if Game.playerBoard[i][j - 1] == "S" or Game.playerBoard[i][j - 1] == " ":
                                # This checks to see if it can fire above the target.
                                Game.ai_move(i, j - 1)
                                has_hit = True
                                break

                        elif j < 10:
                            if Game.playerBoard[i][j + 1] == "S" or Game.playerBoard[i][j + 1] == " ":
                                # This checks to see if it can fire below the target.
                                Game.ai_move(i, j + 1)
                                has_hit = True
                                break
            if not has_hit:  # If all possibilities are exhausted and no hits have been found, the AI will randomly
                # generate a move.
                while True:
                    randx = random.randint(0, 9)
                    randy = random.randint(0, 9)
                    if Game.playerBoard[randx][randy] == "S" or Game.playerBoard[randx][randy] == " ":
                        Game.ai_move(randx, randy)
                        break
