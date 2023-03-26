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
            board = self.getPureBoard()
            print(board)
        else:
            print("Nope")

    def getPureBoard(self):
        board = self.engine.get_board_visual()
        board = board.translate({ord(i): None for i in '+-|'})
        board = board.translate({ord('\n'): None})
        i = 0
        j = 1
        pureBoard = []
        for sign in board:
            if i == j:
                pureBoard.append(sign)
                j += 3
            i += 1

        return pureBoard
