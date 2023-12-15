import pygame
from mazemanager import MazeManager
from gui import GUI

pygame.init()

# pygame.mixer.init()
# pygame.mixer.music.load('audio_file.wav')
# pygame.mixer.music.play(0)

# To loop the audio file indefinitely, uncomment the line below
# pygame.mixer.music.play(-1)

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Maze')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
BG = pygame.image.load("BG.jpeg")

gui = GUI(SCREEN, BG, WIDTH, HEIGHT)
algorithm, rows, cols = gui.main_menu()
manager = MazeManager(SCREEN, rows, cols, WIDTH, HEIGHT)
maze = manager.create_maze()
manager.play(algorithm)
