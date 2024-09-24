import pygame

from data.classes.board import Board
from data.classes.pieces import Piece

pygame.init()

WINDOW_SIZE = (600, 600)
print(WINDOW_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
tiles = 4
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], tiles)

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()


if __name__ == '__main__':
	running = True
	piece = Piece((0, 0), 'white', board)
	piece.draw_flat_stone(1, 1, board, screen)
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
       			# If the mouse is clicked
				if event.button == 1:
					board.handle_click(mx, my)
		# Draw the board
		draw(screen)