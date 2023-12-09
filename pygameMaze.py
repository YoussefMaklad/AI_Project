import pygame
from colors import *


class Cell:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.x = row * width
        self.y = col * height
        self.color = WHITE
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    def is_obstacle(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == WHITE

    def is_visited(self):
        return self.color == RED

    def is_start(self):
        return self.color == LABANY

    def is_goal(self):
        return self.color == GREEN

    def make_obstacle(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE

    def make_visited(self):
        self.color = RED

    def make_explored(self):
        self.color = GREEN

    def make_start(self):
        self.color = LABANY

    def make_goal(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def expand(self, maze):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not maze[self.row + 1][self.col].is_obstacle(): # down
            self.neighbours.append(maze[self.row + 1][self.col])

        if self.row > 0 and not maze[self.row - 1][self.col].is_obstacle(): # up
            self.neighbours.append(maze[self.row - 1][self.col])

        if self.col > 0 and not maze[self.row][self.col - 1].is_obstacle(): # left
            self.neighbours.append(maze[self.row][self.col - 1])

        if self.col < self.total_cols - 1 and not maze[self.row][self.col + 1].is_obstacle(): # right
            self.neighbours.append(maze[self.row][self.col + 1])


class MazeManager:
    def __init__(self):
        self.fringe = []
        self.visited = set()

    def create_maze(self, rows, cols, width, height):
        maze = []
        gap_row = width // rows
        gap_col = height // cols
        for i in range(rows):
            maze.append([])
            for j in range(cols):
                cell = Cell(i, j, gap_row, gap_col, rows, cols)
                maze[i].append(cell)
        return maze

    def draw_maze(self, screen, rows, cols, width, height):
        gap_row = width // rows
        gap_col = height // cols
        for i in range(rows):
            pygame.draw.line(screen, GREY, (0, i * gap_row), (width, i * gap_row))
            for j in range(cols):
                pygame.draw.line(screen, GREY, (j * gap_col, 0), (j * gap_col, width))

    def draw_scene(self, screen, maze, rows, cols, width, height):
        screen.fill(WHITE)
        for i in range(rows):
            for j in range(cols):
                maze[i][j].draw(screen)
        self.draw_maze(screen, rows, cols, width, height)
        pygame.display.update()

    def get_clicked_pos(self, pos, rows, cols, width, height):
        gap_row = width // rows
        gap_col = height // cols
        y, x = pos
        row = y // gap_row
        col = x // gap_col
        return row, col

    def astar(self, draw_scene, maze, start, goal):
        pass


WIDTH = HEIGHT = 800
ROWS = 50
COLS = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze')
icon = pygame.image.load('maze.png')
pygame.display.set_icon(icon)

manager = MazeManager()
maze = manager.create_maze(ROWS, COLS, WIDTH, HEIGHT)

start = None
goals = []
while True:
    manager.draw_scene(screen, maze, ROWS, COLS, WIDTH, HEIGHT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(ROWS):
                    for j in range(COLS):
                        maze[i][j].expand(maze)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = manager.get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
            cell = maze[row][col]
            if not start and cell not in goals:
                start = cell
                cell.make_start()
            elif cell != start and cell not in goals:
                cell.make_obstacle()
        elif pygame.mouse.get_pressed()[1]:
            pos = pygame.mouse.get_pos()
            row, col = manager.get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
            cell = maze[row][col]
            if cell not in goals:
                cell.make_goal()
                goals.append(cell)
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = manager.get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
            cell = maze[row][col]
            cell.reset()
            if cell == start:
                start = None
            if cell in goals:
                cell = None
    pygame.display.update()
