

class Game():
    def __init__(self):
        self.board = [[0] * 8] * 8

class Piece():
    def __init__(self, position):
        self.position = position
    
class Pawn(Piece):
    pass

