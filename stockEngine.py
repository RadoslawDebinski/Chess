from stockfish import Stockfish


class StockEngine():

    def __init__(self, stockPath):
        self.stockPath = stockPath
        self.engine = Stockfish(path=self.stockPath, depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
        self.moves = []

    def move(self, move):
        move = str(move)
        if self.engine.is_move_correct(move):
            self.moves.append(move)
            self.engine.set_position(self.moves)
            board = self.engine.get_board_visual()
            print(board)
        else:
            print("Nope")

