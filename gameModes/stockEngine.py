from stockfish import Stockfish


class StockEngine:

    def __init__(self, stockPath):
        self.stockPath = stockPath
        self.engine = Stockfish(path=self.stockPath, depth=18,
                                parameters={"UCI_Elo": 3000, "Hash": 8, "Threads": 4, "Minimum Thinking Time": 30})
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

    def getEvaluation(self, fen):
        if self.engine.is_fen_valid(fen):
            self.engine.set_fen_position(fen)
            return self.engine.get_evaluation()
        else:
            return {"type": "cp", "value": 0}

    def getPureBoard(self):
        board = self.engine.get_board_visual()

        board = board.translate({ord(i): None for i in '+-|'})
        board = board.translate({ord('\n'): None})

        pureBoard = [sign for i, sign in enumerate(board) if (i + 2) % 3 == 0]

        return pureBoard
