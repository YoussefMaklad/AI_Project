import random
import pyamaze
from pyamaze import agent, COLOR


def uninformed_search_decorator(func):
    def wrapper(maze: pyamaze.maze, goal: tuple):
        start = (maze.rows, maze.cols)
        algorithm, fringe, visited, path = '', [start], set(), {}
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
            if cell == goal:
                break
            for move in "ESNW":
                if maze.maze_map[cell][move] == 1:
                    child_cell = check_move(cell, move)
                    if child_cell in visited:
                        continue
                    visited.add(child_cell)
                    fringe.append(child_cell)
                    path[child_cell] = cell
        fwd_path = {}
        cell = goal
        while cell != start:
            fwd_path[path[cell]] = cell
            cell = path[cell]
        return fwd_path
    return wrapper


def check_move(cell, move):
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
def dfs(maze: pyamaze.maze, goal: tuple):
    pass


@uninformed_search_decorator
def bfs(maze: pyamaze.maze, goal: tuple):
    pass


if __name__ == '__main__':
    maze = pyamaze.maze(20, 20)
    goal = (random.randint(1,20), random.randint(1, 20))
    maze.CreateMaze(goal[0], goal[1], loopPercent=0, theme=COLOR.dark)
    path_dfs = dfs(maze, goal)
    path_bfs = bfs(maze, goal)
    a = agent(maze, footprints=True, color=COLOR.blue)
    b = agent(maze, footprints=True, color=COLOR.red)
    maze.tracePath({a: path_dfs}, delay=100)
    maze.tracePath({b: path_bfs}, delay=100)
    maze.run()
