from collections import deque as queue


class Graph:

    def __init__(self, edges, costs, goals):
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

    def dfs(self, start):
        visited, fringe = set(), list([[start]])
        while fringe:
            path = fringe.pop()
            node = path[-1]
            if self.check_goal(node):
                return path
            else:
                if tuple(node) not in visited:
                    visited.add(tuple(node))
                    fringe.extend(self.expand_dfs(node, path))
        return None

    def heuristic(self, current_node):
        if current_node in self.heuristic_dict:
            return self.heuristic_dict[current_node]
        if self.check_goal(current_node):
            heuristic_value = 0
        else:
            cumulative_cost = 0
            node = current_node
            while node not in self.goals:
                neighbors = self.graph_dict.get(str(node), [])
                if not neighbors:
                    return float('inf')
                next_node, _ = min(
                    [(neighbor, self.costs.get((node, neighbor), float('inf')) + self.heuristic(neighbor))
                     for neighbor in neighbors],
                    key=lambda x: x[1]
                )
                cumulative_cost += self.costs.get((node, next_node), 0)
                node = next_node
            heuristic_value = cumulative_cost
        self.heuristic_dict[current_node] = heuristic_value
        return heuristic_value

    @expand_heuristic_decorator
    def expand_greedy(self, node, path):
        pass

    def greedy(self, start):
        self.heuristic(start)
        visited, fringe, path = set(), [], []
        node = start
        fringe.append((self.heuristic_dict[node], node))
        while fringe:
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
        return None

    @expand_heuristic_decorator
    def expand_astar(self, node, path):
        pass

    def astar(self, start):
        self.heuristic(start)
        visited, fringe, path = set(), [], []
        node = start
        fringe.append((self.heuristic_dict[node] + 0, node))
        while fringe:
            print(fringe)
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
        return None

    def path_cost(self, path):
        return sum(self.costs.get((path[i], path[i + 1]), 1) for i in range(len(path) - 1))

    def ucs(self, start):
        visited, fringe = set(), [(0, start, [])]
        while fringe:
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
        return None


edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "G"), ("D", "G")]
costs = {
    ("A", "B"): 1,
    ("A", "C"): 4,
    ("B", "D"): 2,
    ("C", "D"): 1,
    ("D", "E"): 5,
    ("E", "G"): 2,
    ("D", "G"): 1
}
g = Graph(edges, costs, ["G"])

# print(g.bfs("A"))
# print(g.dfs("A"))
# print(g.ucs("A"))
# print(g.greedy("A"))
# print(g.astar("A"))
