from graphProject import Graph

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
heuristic = {"A": 5, "B": 15, "C": 1, "D": 20, "E": 0, "G": 1000}
g = Graph(edges, costs, heuristic, ["G"])


def calling_function(edge, cost, heuristic, strategy, start, goal):
    g = Graph(edge, cost, heuristic, goal)
    match strategy:
        case "ucs":
            visited, fringe = set(), [(0, start, [])]
            while fringe:
                ans = g.ucs(fringe, visited)
                if ans:
                    break
            if ans:
                return ans
            return None
        case "bfs":
            action - 2
        case "dfs":
            visited, fringe = set(), list([[start]])
            while fringe:
                # print(fringe)
                ans = g.dfs(fringe, visited)
                if ans:
                    break
            if ans:
                return ans
            return ans
        case "greedy":
            visited, fringe = set(), []
            fringe.append((g.heuristic_dict[start], start))
            while fringe:
                ans = g.greedy(fringe, visited)
                if ans:
                    break
            if ans:
                return ans
            return None
        case "astar":
            visited, fringe = set(), []
            fringe.append((g.heuristic_dict[start] + 0, start))
            while fringe:
                ans = g.astar(fringe, visited)
                if ans:
                    break
            if ans:
                return ans
            return None


print(calling_function(edges, costs, heuristic, "dfs", "A", "G"))
