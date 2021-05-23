from board import Board
from tkinter import *
from PIL import ImageTk, Image
from pieces import *


root = Tk()
root.geometry('1000x600')
# root.iconbitmap('file.ico')

canvas = Canvas(root, width=520, height=520, bg='white', bd=-2)
canvas.pack()

board = Board(canvas)
board.draw_board()
board.setup()

# root.attributes('-fullscreen',True)
root.mainloop()
