# Imports the Pygame and Time modules as well as the Board file
import pygame, time
from pygame.locals import *
import Board

# Starts the Pygame module
pygame.init()
pygame.mixer.quit()


# Sets the width and height of the Pygame window and then creates it
width = 800
height = 800
screen = pygame.display.set_mode((width, height))

board = Board.Board()

def update():
    board.show(screen)

# Main game loop
while True:
    time.sleep(0.0166)
    # Checks for user inputs
    for event in pygame.event.get():
        # Checks if the user has closed the window, if so end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            update()
            board.update()
    update()
    pygame.display.flip()