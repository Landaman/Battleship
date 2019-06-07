# This is the AI Control, both board setup and actual moves
class AI:  # This is the AI class.
    def __init__(self, difficulty):
        import Game
        import UIControl
        self.difficulty = difficulty
        self.ships = []
        self.ships.append(Game.Ship(UIControl.board.AIShips, Game.AIBoard, UIControl.board.AIBoard, 5, 0,
                                    UIControl.shipImg1))
        self.ships.append(Game.Ship(UIControl.board.AIShips, Game.AIBoard, UIControl.board.AIBoard, 4, 0,
                                    UIControl.shipImg2))
        self.ships.append(Game.Ship(UIControl.board.AIShips, Game.AIBoard, UIControl.board.AIBoard, 3, 0,
                                    UIControl.shipImg3))
        self.ships.append(Game.Ship(UIControl.board.AIShips, Game.AIBoard, UIControl.board.AIBoard, 4, 1,
                                    UIControl.shipImg4))
        self.ships.append(Game.Ship(UIControl.board.AIShips, Game.AIBoard, UIControl.board.AIBoard, 2, 1,
                                    UIControl.shipImg5))

    def gen_board(self):
        import random
        for i in range(len(self.ships)):
            while True:
                if self.difficulty == 1:
                    randx = random.randint(0, 9)
                    randy = random.randint(0, 9)
                elif self.difficulty == 2:
                    randx = random.randint(1, 8)
                    randy = random.randint(1, 8)
                else:
                    randx = random.randint(2, 7)
                    randy = random.randint(2, 7)
                if self.ships[i].check_place(randx, randy):
                    self.ships[i].board_place(randx, randy)
                    break

    def get_hit(self):
        import random
        import Game
        if self.difficulty == 1:
            while True:
                randx = random.randint(0, 9)
                randy = random.randint(0, 9)
                if Game.playerBoard[randx][randy] == "S" or Game.playerBoard[randx][randy] == " ":
                    Game.ai_move(randx, randy)
                    break
        else:
            has_hit = False
            for i in range(10):
                for j in range(10):
                    if Game.playerBoard[i][j] == "H":
                        if i > 0:
                            if Game.playerBoard[i - 1][j] == "S" or Game.playerBoard[i - 1][j] == " ":
                                Game.ai_move(i - 1, j)
                                has_hit = True
                                break
                        elif i < 10:
                            if Game.playerBoard[i + 1][j] == "S" or Game.playerBoard[i + 1][j] == " ":
                                Game.ai_move(i + 1, j)
                                has_hit = True
                                break
                        elif j > 0:
                            if Game.playerBoard[i][j - 1] == "S" or Game.playerBoard[i][j - 1] == " ":
                                Game.ai_move(i, j - 1)
                                has_hit = True
                                break

                        elif j < 10:
                            if Game.playerBoard[i][j + 1] == "S" or Game.playerBoard[i][j + 1] == " ":
                                Game.ai_move(i, j + 1)
                                has_hit = True
                                break
            if not has_hit:
                while True:
                    randx = random.randint(0, 9)
                    randy = random.randint(0, 9)
                    if Game.playerBoard[randx][randy] == "S" or Game.playerBoard[randx][randy] == " ":
                        Game.ai_move(randx, randy)
                        break
