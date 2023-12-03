import random
import pyamaze
from pyamaze import agent, COLOR


class MazeManager:
    def __init__(self, maze: pyamaze.maze):
        self.maze = maze

    @staticmethod
    def uninformed_search_decorator(func):
        def wrapper(self):
            start = (self.maze.rows, self.maze.cols)
            algorithm, fringe, visited, path, search = '', [start], set(), {}, []
            visited.add(start)
            if func.__name__ == 'bfs':
                algorithm = 'bfs'
            else:
                algorithm = 'dfs'
            while fringe:
                if algorithm == 'dfs':
                    cell = fringe.pop(-1)
                else:
                    cell = fringe.pop(0)
                search.append(cell)
                count_mark = 0
                if cell == self.maze._goal:
                    break
                for move in "ESNW":
                    if self.maze.maze_map[cell][move] == 1:
                        child_cell = self.check_move(cell, move)
                        if child_cell in visited:
                            continue
                        visited.add(child_cell)
                        fringe.append(child_cell)
                        path[child_cell] = cell
                        count_mark += 1
                if count_mark > 1:
                    self.maze.markCells.append(cell)
            fwd_path = {}
            cell = self.maze._goal
            while cell != start:
                fwd_path[path[cell]] = cell
                cell = path[cell]
            return fwd_path, search
        return wrapper

    def check_move(self, cell, move):
        child_cell = None
        match move:
            case 'E':
                child_cell = (cell[0], cell[1] + 1)
            case 'W':
                child_cell = (cell[0], cell[1] - 1)
            case 'S':
                child_cell = (cell[0] + 1, cell[1])
            case 'N':
                child_cell = (cell[0] - 1, cell[1])
        return child_cell

    @uninformed_search_decorator
    def dfs(self):
        pass

    @uninformed_search_decorator
    def bfs(self):
        pass


if __name__ == '__main__':
    maze = pyamaze.maze(15, 15)
    goal = (random.randint(1, 15), random.randint(1, 15))
    maze.CreateMaze(goal[0], goal[1], loopPercent=200, theme=COLOR.dark)
    maze_manager = MazeManager(maze)
    path_dfs, search_dfs = maze_manager.dfs()
    path_bfs, search_bfs = maze_manager.bfs()
    a = agent(maze, filled=True, footprints=True, color=COLOR.blue)
    b = agent(maze, footprints=True, color=COLOR.green)
    c = agent(maze, filled=True, footprints=True, color=COLOR.yellow)
    d = agent(maze, footprints=True, color=COLOR.red)
    maze.tracePath({b: search_dfs}, showMarked=True, delay=100)
    maze.tracePath({a: path_dfs}, delay=100, kill=True)
    maze.tracePath({d: search_bfs}, showMarked=True, delay=100)
    maze.tracePath({c: path_bfs}, delay=100)
    maze.run()
