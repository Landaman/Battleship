# This is the AI Control, both board setup and actual moves
class AI:  # This is the AI class.
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def gen_board(self):
        if self.difficulty == 1:
            print("h")