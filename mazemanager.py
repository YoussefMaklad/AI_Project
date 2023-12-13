import random

import pygame
from collections import deque as queue
from cell import Cell
from colors import *


class MazeManager:
    def __init__(self, screen, rows, cols, width, height):
        self.screen = screen
        self.maze = []
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.heuristic_dict = dict()

    def expand(self, cell: Cell):
        cell.neighbours = []
        if cell.row < cell.total_rows - 1 and not self.maze[cell.row + 1][cell.col].is_obstacle(): # down
            cell.neighbours.append(self.maze[cell.row + 1][cell.col])

        if cell.row > 0 and not self.maze[cell.row - 1][cell.col].is_obstacle(): # up
            cell.neighbours.append(self.maze[cell.row - 1][cell.col])

        if cell.col > 0 and not self.maze[cell.row][cell.col - 1].is_obstacle(): # left
            cell.neighbours.append(self.maze[cell.row][cell.col - 1])

        if cell.col < cell.total_cols - 1 and not self.maze[cell.row][cell.col + 1].is_obstacle(): # right
            cell.neighbours.append(self.maze[cell.row][cell.col + 1])

        return cell.neighbours

    def create_maze(self):
        gap_row = self.height // self.rows  # Corrected
        gap_col = self.width // self.cols  # Corrected
        for i in range(self.rows):
            self.maze.append([])
            for j in range(self.cols):
                cell = Cell(i, j, gap_row, gap_col, self.rows, self.cols)
                self.maze[i].append(cell)
        return self.maze

    def draw_maze(self):
        gap_row = self.height // self.rows  # Corrected
        gap_col = self.width // self.cols  # Corrected
        for i in range(self.rows):
            pygame.draw.line(self.screen, GREY, (0, i * gap_row), (self.width, i * gap_row))
            for j in range(self.cols):
                pygame.draw.line(self.screen, GREY, (j * gap_col, 0), (j * gap_col, self.height))

    def draw_scene(self):
        self.screen.fill(WHITE)
        for i in range(self.rows):
            for j in range(self.cols):
                self.maze[i][j].draw(self.screen)
        self.draw_maze()
        pygame.display.update()

    def get_clicked_pos(self, pos):
        gap_row = self.height // self.rows
        gap_col = self.width // self.cols
        x, y = pos
        col = y // gap_row
        row = x // gap_col
        return row, col

    def bfs(self, start, goals):
        fringe, visited, path = queue(), set(), []
        paths_dict = {start: None}
        fringe.append(start)
        while fringe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            node = fringe.popleft()
            if node in goals:
                self.visualize_path(node, paths_dict)
                return
            if node not in visited:
                visited.add(node)
                node.make_visited()
                neighbors = self.expand(node)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        fringe.append(neighbor)
                        neighbor.make_explored()
                        paths_dict[neighbor] = node
            self.draw_scene()

    def dfs(self, start, goals):
        fringe, visited, path = [], set(), []
        paths_dict = {start: None}
        fringe.append([start])
        while fringe:
            print("Start:")
            for lst_1 in fringe:
                for cell in lst_1:
                    print(cell.row,cell.col)
                print("=======================================")
            print("End\n")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if fringe[0] == [start]:
                node = fringe.pop(-1)
                node = node[0]
            else:
                lst = fringe.pop(-1)
                node = random.choice(lst)
                lst.remove(node)
                if len(lst) != 0:
                    fringe.append(lst)
            if node in goals:
                self.visualize_path(node, paths_dict)
                return
            if node not in visited:
                visited.add(node)
                node.make_visited()
                neighbors = self.expand(node)
                final_neighbour = []
                for neighbor in neighbors:
                    if neighbor not in visited:
                        final_neighbour.append(neighbor)
                        neighbor.make_explored()
                        paths_dict[neighbor] = node
                if len(final_neighbour) > 0:
                    fringe.append(final_neighbour)
            self.draw_scene()
            pygame.time.delay(500)

    def astar(self, start, goals):
        pass

    def visualize_path(self, goal, paths_dict):
        path, current_node = [], goal
        while current_node:
            path.append(current_node)
            current_node = paths_dict[current_node]
        path = path[::-1]
        for current_node in path:
            current_node.make_path()
            self.draw_scene()

    def play(self, algorithm):
        start = None
        goals = []
        while True:
            self.screen.fill("Black")
            self.draw_scene()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        match algorithm:
                            case 'bfs':
                                self.bfs(start, goals)
                            case 'dfs':
                                self.dfs(start, goals)
                            case 'astar':
                                self.astar(start, goals)

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    if row is not None and col is not None:
                        cell = self.maze[row][col]
                        if not start and cell not in goals:
                            start = cell
                            cell.make_start()
                        elif cell != start and cell not in goals:
                            cell.make_obstacle()
                elif pygame.mouse.get_pressed()[1]:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    cell = self.maze[row][col]
                    if cell not in goals:
                        cell.make_goal()
                        goals.append(cell)
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    cell = self.maze[row][col]
                    cell.reset()
                    if cell == start:
                        start = None
                    if cell in goals:
                        goals.remove(cell)
            pygame.display.update()
