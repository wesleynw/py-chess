from PIL import ImageTk, Image

class Piece():
    def __init__(self, type, color):
        self.image_id = None
        self.color = color
        self.texture = ImageTk.PhotoImage(Image.open('assets/'+type+'_' + color + '.png').resize((65, 65)))
    # def can_move_to(self, board, x, y):
    #     return self.on_board(x, y) and board.squares[x][y].piece 
    def on_board(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

class Pawn(Piece):
    name = 'pawn'
    def __init__(self, color):
        super().__init__('pawn', color)

    def actions(self, board, coords, passive = False):
        x, y = coords
        moves, captures = [], []
        guarded = board.guarded_places() if not passive else []
        if board.move_will_put_in_check(x, y, guarded):
            return moves, captures
        if self.color == 'w':
            if super().on_board(x, y - 1) and not board.squares[x][y - 1].piece:
                moves.append((x, y - 1))
            if y == 6 and super().on_board(x, y - 2) and not board.squares[x][y - 2].piece:
                moves.append((x, y - 2))

            if super().on_board(x - 1, y - 1) and board.squares[x - 1][y - 1].piece and board.squares[x - 1][y - 1].piece.color != board.turn:
                captures.append((x - 1, y - 1))
            if super().on_board(x + 1, y - 1) and board.squares[x + 1][y - 1].piece and board.squares[x + 1][y - 1].piece.color != board.turn:
                captures.append((x + 1, y - 1))  
        else:
            if super().on_board(x, y + 1) and not board.squares[x][y + 1].piece:
                moves.append((x, y + 1))
            if y == 1 and super().on_board(x, y + 2) and not board.squares[x][y + 2].piece:
                moves.append((x, y + 2))
            
            if super().on_board(x - 1, y + 1) and board.squares[x - 1][y + 1].piece and board.squares[x - 1][y + 1].piece.color != board.turn:
                captures.append((x - 1, y + 1))
            if super().on_board(x + 1, y + 1) and board.squares[x + 1][y + 1].piece and board.squares[x + 1][y + 1].piece.color != board.turn:
                captures.append((x + 1, y + 1))  
        
        return moves, captures
            



class Rook(Piece):
    name = 'rook'
    def __init__(self, color):
        super().__init__('rook', color)
    def actions(self, board, coords, passive = False):
        x, y = coords
        moves, captures = [], []

        guarded = board.guarded_places() if not passive else []
        if board.move_will_put_in_check(x, y, guarded):
            return moves, captures

        # right
        for n in range(1,8):
            if not Piece.on_board(self, x + n, y):
                break
            elif board.squares[x + n][y].piece:
                captures.append((x + n, y)) if board.squares[x + n][y].piece.color != board.turn else True
                break
            else:
                moves.append((x + n, y))
        # left 
        for n in range(1,8):
            if not Piece.on_board(self, x - n, y):
                break
            elif board.squares[x - n][y].piece:
                captures.append((x - n, y)) if board.squares[x - n][y].piece.color != board.turn else True
                break
            else:
                moves.append((x - n, y))
        # up 
        for n in range(1,8):
            if not Piece.on_board(self, x, y - n):
                break
            elif board.squares[x][y - n].piece:
                captures.append((x, y - n)) if board.squares[x][y - n].piece.color != board.turn else True
                break
            else:
                moves.append((x, y - n))
        #down
        for n in range(1,8):
            if not Piece.on_board(self, x, y + n):
                break
            elif board.squares[x][y + n].piece:
                captures.append((x, y + n)) if board.squares[x][y + n].piece.color != board.turn else True
                break
            else:
                moves.append((x, y + n))
                
        return moves, captures

class Knight(Piece):
    name = 'knight'
    def __init__(self, color):
        super().__init__('knight', color)
    def actions(self, board, coords, movement = False):
        x, y = coords
        moves, captures = [], []

        guarded = board.guarded_places() if not movement else []
        if board.move_will_put_in_check(x, y, guarded):
            return moves, captures

        def helper(board, x, y):
            if Piece.on_board(self, x, y):
                if board.squares[x][y].piece and board.squares[x][y].piece.color != board.turn:
                    captures.append((x, y))
                elif not board.squares[x][y].piece:
                    moves.append((x, y))
        helper(board, x - 2, y + 1)
        helper(board, x - 2, y - 1) 
        helper(board, x - 1, y - 2)
        helper(board, x - 1, y + 2)
        helper(board, x + 1, y - 2)
        helper(board, x + 1, y + 2)
        helper(board, x + 2, y - 1)
        helper(board, x + 2, y + 1)
        return moves, captures

class Bishop(Piece):
    name = 'bishop'
    def __init__(self, color):
        super().__init__('bishop', color)
    def actions(self, board, coords, movement = False):
        x, y = coords
        moves, captures = [], []

        guarded = board.guarded_places() if not movement else []
        if board.move_will_put_in_check(x, y, guarded):
            return moves, captures

        for n in range(1, 8):
            if not Piece.on_board(self, x - n, y + n):
                break
            elif board.squares[x - n][y + n].piece:
                captures.append((x - n, y + n)) if board.squares[x - n][y + n].piece.color != board.turn else True
                break
            else:
                moves.append((x - n, y + n))
        for n in range(1, 8):
            if not Piece.on_board(self, x + n, y + n):
                break
            elif board.squares[x + n][y + n].piece:
                captures.append((x + n, y + n)) if board.squares[x + n][y + n].piece.color != board.turn else True
                break
            else:
                moves.append((x + n, y + n))
        for n in range(1, 8):
            if not Piece.on_board(self, x + n, y - n):
                break
            elif board.squares[x + n][y - n].piece:
                captures.append((x + n, y - n)) if board.squares[x + n][y - n].piece.color != board.turn else True
                break
            else:
                moves.append((x + n, y - n))
        for n in range(1, 8):
            if not Piece.on_board(self, x - n, y - n):
                break
            elif board.squares[x - n][y - n].piece:
                captures.append((x - n, y - n)) if board.squares[x - n][y - n].piece.color != board.turn else True
                break
            else:
                moves.append((x - n, y - n))
        return moves, captures


class Queen(Piece):
    name = 'queen'
    def __init__(self, color):
        super().__init__('queen', color)

    def actions(self, board, coords, movement = False):
        x, y = coords
        moves, captures = [], []

        guarded = board.guarded_places() if not movement else []
        if board.move_will_put_in_check(x, y, guarded):
            return moves, captures

        straight = Rook.actions(self, board, coords, movement)
        diagonal = Bishop.actions(self, board, coords, movement)

        return tuple(x + y for x, y in zip(straight, diagonal))


class King(Piece):
    name = 'king'
    def __init__(self, color):
        super().__init__('king', color)

    def actions(self, board, coords, movement = False):
        x, y = coords
        moves, captures = [], []

        # calculate guarded with king removed
        board.squares[x][y].piece = None
        guarded = board.guarded_places() if not movement else []
        board.squares[x][y].piece = self
    
        def helper(self, x, y):
            if super().on_board(x, y) and (x, y) not in guarded:
                if board.squares[x][y].piece and board.squares[x][y].piece.color != board.turn:
                    captures.append((x, y))
                elif not board.squares[x][y].piece:
                    moves.append((x, y))
        
        helper(self, x - 1, y - 1)
        helper(self, x, y - 1)
        helper(self, x + 1, y - 1)
        helper(self, x - 1, y)
        helper(self, x + 1, y)
        helper(self, x - 1, y + 1)
        helper(self, x, y + 1)
        helper(self, x + 1, y + 1)
        return moves, captures