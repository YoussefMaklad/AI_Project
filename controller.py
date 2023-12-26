from graph import Graph
from collections import deque as queue

edges = [
    ("S", "B"),
    ("S", "A"),
    ("B", "C"),
    ("A", "D"),
    ("G", "D"),
    ("B", "E"),
    ("E", "G"),
    ("C", "G"),
]
costs = {
    ("S", "B"): 2,
    ("S", "A"): 10,
    ("B", "C"): 1,
    ("A", "D"): 5,
    ("G", "D"): 6,
    ("B", "E"): 2,
    ("E", "G"): 4,
    ("C", "G"): 1,
}
heuristic = {"A": 5, "B": 15, "C": 1, "D": 20, "E": 0, "G": 1000}
g = Graph(edges, costs, heuristic, "G")

def calling_function(edge, cost, heuristic, strategy, start, goal):
    g = Graph(edge, cost, heuristic, goal)
    match strategy:
        case "ucs":
            visited, fringe, sortedVisit = set(), [(0, start, [])], []
            while fringe:
                ans = g.ucs(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans
            return None
        case "bfs":
            visited, fringe, sortedVisit = set(), queue([[start]]), []
            while fringe:
                ans = g.bfs(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans
            return ans
        case "dfs":
            visited, fringe, sortedVisit = set(), list([[start]]), []
            while fringe:
                ans = g.dfs(fringe, visited, sortedVisit)
                print(visited)
                if ans:
                    break
            if ans:
                return ans
            return ans
        case "greedy":
            visited, fringe, sortedVisit = set(), [], []
            fringe.append((g.heuristic_dict[start], start))
            while fringe:
                ans = g.greedy(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans
            return None
        case "astar":
            visited, fringe, sortedVisit = set(), [], []
            fringe.append((g.heuristic_dict[start] + 0, start))
            while fringe:
                ans = g.astar(fringe, visited, sortedVisit)
                if ans:
                    break
            if ans:
                return ans
            return None


print(calling_function(edges, costs, heuristic, "bfs", "S", "G"))
