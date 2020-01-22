import os
import random

from tkinter import *
from PIL import Image, ImageTk

photos = {}

class Cell:
	"""A square in Minesweeper"""
	def __init__(self, gui, x, y, board, default_image='tile'):
		self.revealed = False
		self.value = 0
		self.flagged = False
		self.gui = gui
		self.default_image = default_image

		#Register piece
		self.button = Button(gui, image=photos[default_image], borderwidth=0, command=lambda: board.press(x,y))
		self.button.grid(row=1+y, column=x)

	def reveal(self):
		self.revealed = True
		if self.value == 'B':
			photo = photos['mine-clicked']
		elif self.value == 0:
			photo = photos['empty']
		else:
			photo = photos[str(self.value)]

		self.button.configure(image=photo, state=DISABLED)

	def flag(self):
		if not self.flagged:
			self.flagged = True
			self.button.configure(image=photos['flag']) 
		else:
			self.flagged = False
			self.button.configure(image=photos[self.default_image])

	def reset(self):
		self.revealed = False
		self.value = 0
		self.flagged = False
		self.button.configure(image=photos[self.default_image], state=NORMAL)
		

class Board:
	"""A minesweeper board"""
	def __init__(self, difficulty, size):
		#Initialize GUI
		self.gui = Tk()
		self.gui.title("Minesweeper!")
		self.gui.resizable(False, False)

		#Create buttons
		new_game = Button(self.gui, text='New Game', fg='black', height=1, width=8, command=lambda: self.reset())
		self.change_state = Button(self.gui, text='Flag', fg='black', height=1, width=7, command=lambda: self.__change_state()) 
		new_game.grid(row=0, column=0, columnspan=4)
		self.change_state.grid(row=0, column=4, columnspan=4)


		#Set up images
		for file in os.listdir('images'):
			#Store file name & photo ref
			photos[re.sub(r'\..*', '', file)] = ImageTk.PhotoImage(Image.open('images/' + file))

		#Create board layout
		self.sizex, self.sizey = self.__get_size(size)
		self.mines = self.__get_num_mines(difficulty)


		self.board = [[Cell(self.gui, j, i, self) for i in range(self.sizey)] for j in range(self.sizex)]
		self.state = 'reveal'
		self.__place_mines()

	
	def init(self):
		self.gui.mainloop()


	def __is_valid_cell(self, x, y):
		return x in range(self.sizex) and y in range(self.sizey)

	def __add_count(self, x, y):
		position = [
		[-1,-1], 	[0, -1], 	[1, -1],
		[-1, 0], 		  		[1, 0],
		[-1, 1], 	[0, 1],		[1, 1]
		]

		for pos in position:
			pos[0] += x
			pos[1] += y

			if self.__is_valid_cell(pos[0], pos[1]):
				if self.board[pos[0]][pos[1]].value != 'B':
					self.board[pos[0]][pos[1]].value += 1

	def __change_state(self):
		if self.state == 'reveal':
			self.state = 'flag'
			self.change_state.configure(text='Reveal')
		else:
			self.state = 'reveal'
			self.change_state.configure(text='Flag')


	def __place_mines(self):
		mines = self.mines

		while mines > 0:
			x = random.randint(0, self.sizex-1)
			y = random.randint(0, self.sizey-1)

			if self.board[x][y].value != 'B':
				self.board[x][y].value = 'B'
				self.__add_count(x,y)
				mines -= 1

	def __get_size(self, size):
		if size == 'S':
			return 9,9
		elif size == 'M':
			return 16,16
		else:
			return 16,30

	def __get_num_mines(self, difficulty):
		mines = self.sizex * self.sizey 

		if difficulty == 'E':
			return int(mines * .12)
		elif difficulty == 'M':
			return int(mines * .16)
		else:
			return int(mines * .21)

	def print_board(self):
		board = self.board
		val = None
		for y in range(self.sizey):
			for x in range(self.sizex):
				if board[x][y].value == 'B':
					val = 'B'
				elif board[x][y].value == 0:
					val = '.'
				else:
					val = board[x][y].value

				print(val, end=" ")

			print()

	def reset(self):
		for row in self.board:
			for cell in row:
				cell.reset()

		self.__place_mines()

	
	def press(self, x, y):
		if not self.__is_valid_cell(x,y):
			return

		cell = self.board[x][y]

		if cell.revealed:
			return

		if self.state == 'flag':
			cell.flag()
		else:
			if cell.flagged:
				return
				
			cell.reveal()

			#They messed up
			if cell.value == 'B':
				cell.value = 'GG'
				for row in self.board:
					for cell in row:
						if cell.value == 'GG':
							continue

						#False flag
						if cell.flagged and cell.value != 'B':
							cell.button.configure(image=photos['mine-false'])
						elif not cell.flagged and cell.value == 'B':
							cell.button.configure(image=photos['mine'])

						cell.button.configure(state=DISABLED)

			#Flood reveal
			elif cell.value == 0:
				self.press(x-1, y-1)
				self.press(x-1, y)
				self.press(x-1, y+1)
				self.press(x, y-1)
				self.press(x, y+1)
				self.press(x+1, y-1)
				self.press(x+1, y)
				self.press(x+1, y+1)




board = Board('E', 'M')
board.init()