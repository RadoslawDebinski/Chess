from stockEngine import StockEngine

stockPath = "C:\\Users\\radek\\Downloads\\stockfish-11-win\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe"

if __name__ == '__main__':
    engine = StockEngine(stockPath)

    while True:
        move = input()
        engine.move(move)
