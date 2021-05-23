from tkinter import *
from pieces import *
from copy import deepcopy

class Square():
    def __init__(self, space_id, board_coords, canvas_coords, color):
        self.space_id = space_id
        self.board_coords = board_coords
        self.canvas_coords = canvas_coords
        self.color = color
        self.piece = None

class Board():
    places_coords = [[[] for i in range(8)] for i in range(8)]
    sq_size = 65
    for i in range(8):
        for j in range(8):
            places_coords[i][j] = (i * sq_size, j * sq_size) # (x, y)

    def __init__(self, canvas):
        self.turn = 'w'
        self.canvas = canvas
        self.squares = [[[] for i in range(8)] for i in range(8)]
        self.selected_square = None
        self.selected_action_options = []
        self.highlighted_squares = []

        self.captured = {"w" : [], "b" : []}

    def draw_board(self):
        sq_size = 65 # subject to change
        color = 'white'
        for col in range(8):
            for row in range(8):
                x1, y1, x2, y2 = sq_size * col, sq_size * row, sq_size * (col + 1), sq_size * (row + 1)
                space_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                square = Square(space_id, (col, row), (x1, y1), color)
                self.squares[col][row] = square
                self.canvas.tag_bind(space_id, "<Button>", (lambda square: lambda e: self.on_board_click(square))(square))
                if row != 7:
                    color = 'white' if color == 'grey' else 'grey'

    def on_board_click(self, square):
        # if another piece is clicked
        if square.piece:
            # if the piece clicked is the same color as the turn
            if square.piece.color == self.turn:
                self.clear_highlights()
                self.selected_square = square
                self.selected_action_options = square.piece.actions(self, square.board_coords, False)
                # self.selected_action_options = eval(square.piece.__class__.__name__).actions(square.piece, self, square.board_coords, False)
                self.canvas.itemconfigure(square.space_id, fill='yellow')
                self.highlighted_squares = [square]
                for x, y in self.selected_action_options[0]:
                    self.canvas.itemconfigure(self.squares[x][y].space_id, fill='green')
                    self.highlighted_squares.append(self.squares[x][y])
                for x, y in self.selected_action_options[1]:
                    self.canvas.itemconfigure(self.squares[x][y].space_id, fill='orange')
                    self.highlighted_squares.append(self.squares[x][y])
            # capture a piece 
            elif self.selected_square and square.board_coords in self.selected_action_options[1]:
                self.captured[self.turn].append(square.piece)
                self.canvas.delete(square.piece.image_id)
                square.piece = None
                self.move_piece(square)
                self.clear_highlights()
        elif self.selected_square:
        # a square has been clicked, and a piece has been selected
            if square.board_coords in self.selected_action_options[0]:
                self.move_piece(square)
            for square_h in self.highlighted_squares:
                self.canvas.itemconfigure(square_h.space_id, fill=square_h.color)
            self.highlighted_squares = []

    def move_piece(self, end_square):
        # TODO: animate movement
        # move piece from self.selected to *square*
        x1, y1 = self.selected_square.canvas_coords
        x2, y2 = end_square.canvas_coords
        self.canvas.move(self.selected_square.piece.image_id, x2 - x1, y2 - y1)
        self.canvas.tag_bind(self.selected_square.piece.image_id, '<Button>', (lambda square: lambda e: self.on_board_click(square))(end_square))
        self.selected_square.piece, end_square.piece = None, self.selected_square.piece
        self.selected_square = None
        self.selected_action_options = None
        self.next_turn()

    def clear_highlights(self):
        for square in self.highlighted_squares:
                self.canvas.itemconfigure(square.space_id, fill=square.color)
        self.selected_square = None
        self.selected_action_options = None

    def next_turn(self):
        # TODO: add hinting on the board for the last turn's moves
        self.in_check(self.guarded_places())
        if self.turn == 'w':
            self.turn = 'b'
            # id = self.canvas.create_text(260, 260, anchor='center', text="Black's turn", fill='red')
        else:
            self.turn = 'w'
        
    def guarded_places(self):
        """returns a list of all spaces AND PIECES that are in range for pieces from the other side"""
        guarded = []
        for x in range(8):
            for y in range(8):
                if self.squares[x][y].piece and self.squares[x][y].piece.color != self.turn:
                    squares = self.squares[x][y].piece.actions(self, (x, y), True)
                    if self.squares[x][y].piece.name != 'pawn': # pawns capture in different areas than they move
                        guarded.extend(squares[0])
                    guarded.extend(squares[1])
        return guarded

    def move_will_put_in_check(self, x1, y1, guarded):
        piece_temp = self.squares[x1][y1].piece
        self.squares[x1][y1].piece = None
        b = self.in_check(guarded)
        self.squares[x1][y1].piece = piece_temp
        return b

    def in_check(self, guarded):
        for x, y in guarded:
            s = self.squares[x][y]
            if s.piece and isinstance(s.piece, King) and s.piece.color == self.turn:
                print('123')
                self.canvas.itemconfigure(s.space_id, fill='red')
                # self.highlighted_squares.append(self.squares[x][y])
                return True
        return False

    def setup(self):
        # white 
        self.place_piece(Pawn('w'), 0, 6)
        self.place_piece(Pawn('w'), 1, 6)
        self.place_piece(Pawn('w'), 2, 6)
        self.place_piece(Pawn('w'), 3, 6)
        self.place_piece(Pawn('w'), 4, 6)
        self.place_piece(Pawn('w'), 5, 6)
        self.place_piece(Pawn('w'), 6, 6)
        self.place_piece(Pawn('w'), 7, 6)
        self.place_piece(Rook('w'), 0, 7)
        self.place_piece(Rook('w'), 7, 7)
        self.place_piece(Knight('w'), 1, 7)
        self.place_piece(Knight('w'), 6, 7)
        self.place_piece(Bishop('w'), 2, 7)
        self.place_piece(Bishop('w'), 5, 7)
        self.place_piece(Queen('w'), 3, 7)
        self.place_piece(King('w'), 4, 7)


        # black
        self.place_piece(Pawn('b'), 0, 1)
        self.place_piece(Pawn('b'), 1, 1)
        self.place_piece(Pawn('b'), 2, 1)
        self.place_piece(Pawn('b'), 3, 1)
        self.place_piece(Pawn('b'), 4, 1)
        self.place_piece(Pawn('b'), 5, 1)
        self.place_piece(Pawn('b'), 6, 1)
        self.place_piece(Pawn('b'), 7, 1)
        self.place_piece(Rook('b'), 0, 0)
        self.place_piece(Rook('b'), 7, 0)
        self.place_piece(Knight('b'), 6, 0)
        self.place_piece(Knight('b'), 1, 0)
        self.place_piece(Bishop('b'), 2, 0)
        self.place_piece(Bishop('b'), 5, 0)
        self.place_piece(Queen('b'), 3, 0)
        self.place_piece(King('b'), 4, 0)


    def place_piece(self, piece, x, y):
        x_coord, y_coord = Board.places_coords[x][y][0], Board.places_coords[x][y][1]
        self.squares[x][y].piece = piece
        image_id = self.canvas.create_image(x_coord, y_coord, image=piece.texture, anchor='nw')
        piece.image_id = image_id
        self.canvas.tag_bind(image_id, '<Button>', (lambda square: lambda e: self.on_board_click(square))(self.squares[x][y]))
        if piece.name == 'king':
            self.king = piece