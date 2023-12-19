from collections import deque as queue


class Graph:
    def __init__(self, edges, costs, heuristic, goals):
        self.graph_dict = {}
        self.heuristic_dict = {}
        self.edges = edges
        self.costs = costs
        self.goals = goals
        for start, end in edges:
            if start not in self.graph_dict:
                self.graph_dict[start] = [end]
            else:
                self.graph_dict[start].append(end)
        for node, value in heuristic.items():
            self.heuristic_dict[node] = value

    def check_goal(self, node):
        return True if node in self.goals else False

    @staticmethod
    def expand_decorator(func):
        def wrapper(self, node, path):
            func(self, node, path)
            neighbors = self.graph_dict.get(str(node), [])
            new_path = [path + [element] for element in neighbors]
            return new_path
        return wrapper

    @staticmethod
    def expand_heuristic_decorator(func):
        def wrapper(self, node, path):
            neighbours = self.graph_dict.get(str(node), [])
            if func.__name__ == 'expand_astar':
                new_path = [(self.heuristic_dict[element] + self.path_cost(path) + self.costs.get((node, element)),
                             [i for i in path] + [element]) for element in neighbours]
            else:
                new_path = [(self.heuristic_dict[element], [i for i in path] + [element]) for element in neighbours]
            return new_path

        return wrapper

    @expand_decorator
    def expand_bfs(self, node, path):
        pass

    def bfs(self, start):
        visited, fringe = set(), queue([[start]])
        while fringe:
            path = fringe.popleft()
            node = path[-1]
            if self.check_goal(node):
                return path
            else:
                if tuple(node) not in visited:
                    visited.add(tuple(node))
                    fringe.extend(self.expand_bfs(node, path))
        return None

    @expand_decorator
    def expand_dfs(self, node, path):
        pass

    def dfs(self, fringe, visited):
        if fringe:
            print(fringe)
            path = fringe.pop()
            node = path[-1]
            if self.check_goal(node):
                return path
            else:
                if tuple(node) not in visited:
                    visited.add(tuple(node))
                    fringe.extend(self.expand_dfs(node, path))
        return False

    @expand_heuristic_decorator
    def expand_greedy(self, node, path):
        pass

    def greedy(self, fringe, visited):
        path = []
        if fringe:
            h, node = min(fringe)
            fringe.remove((h, node))
            path = node
            node = node[-1]
            if self.check_goal(node):
                return path
            else:
                if tuple(node) not in visited:
                    visited.add(tuple(node))
                    fringe.extend(self.expand_greedy(node, path))
        return False

    @expand_heuristic_decorator
    def expand_astar(self, node, path):
        pass

    def astar(self, fringe, visited):
        path = []
        if fringe:
            h, node = min(fringe)
            fringe.remove((h, node))
            path = node
            node = node[-1]
            if self.check_goal(node):
                return path
            else:
                if tuple(node) not in visited:
                    visited.add(tuple(node))
                    fringe.extend(self.expand_astar(node, path))
        return False

    def path_cost(self, path):
        return sum(self.costs.get((path[i], path[i + 1]), 1) for i in range(len(path) - 1))

    def ucs(self, fringe, visited):
        if fringe:
            cost, node, path = min(fringe, key=lambda x: x[0])
            fringe.remove((cost, node, path))
            if self.check_goal(node):
                return path + [node]
            else:
                if node not in visited:
                    visited.add(node)
                    for neighbor in self.graph_dict.get(node, []):
                        edge = (node, neighbor)
                        new_cost = cost + self.costs.get(edge, 1)
                        new_path = path + [node]
                        fringe.append((new_cost, neighbor, new_path))
        return False
