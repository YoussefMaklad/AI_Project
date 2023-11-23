from collections import deque as queue
import heapq

class Graph:
    fringeDFS = list()
    fringeGreedy, fringeAStar, fringeUCS = [], [], []
    Visited = set()
    goals = []
    def __init__(self, edges, costs, goals):
        self.edges = edges
        self.costs = costs
        self.graph_dict = {}
        self.goals = goals
        for start, end in edges:
            if start not in self.graph_dict:
                self.graph_dict[start] = [end]
            else:
                self.graph_dict[start].append(end)

    def checkGoal(self, node):
        return True if node in [element for element in self.goals] else False
    def expandBFS(self, node, path):
        neighbours = self.graph_dict.get(str(node),[])
        newPath = [path + [element] for element in neighbours]
        return newPath

    def bfs(self, start):
        self.Visited = set()
        fringe = queue([[start]])
        while fringe:
            # print([element for element in fringe])
            path = fringe.popleft()
            node = path[-1]
            if self.checkGoal(node):
                return path
            else:
                if tuple(node) not in self.Visited:
                    self.Visited.add(tuple(node))
                    fringe.extend(self.expandBFS(node, path))
        return False
    def expandDFS(self, node, path):
        neighbours = self.graph_dict.get(str(node), [])
        newPath = [path + [element] for element in neighbours]
        return newPath


    def dfs(self, start):
        self.Visited = set()
        fringe = list([[start]])
        while fringe:
            path = fringe.pop()
            node = path[-1]
            if self.checkGoal(node):
                return path
            else:
                if tuple(node) not in self.Visited:
                    self.Visited.add(tuple(node))
                    fringe.extend(self.expandDFS(node, path))
        return False

    def calcHeuristic(self, graph):
        pass

    def expandGreedy(self, node):
        # add nodes to fringe here
        pass

    def greedy(self, start):
        self.Visited = set()
        self.calcHeuristic(start)
        node = start
        heapq.heappush(self.fringeGreedy,node)
        while self.fringeGreedy:
            node = heapq.heappop(self.fringeGreedy)
            if self.checkGoal(node):
                return node
            else:
                if node not in self.Visited:
                    self.Visited.add(node)
                    self.expandGreedy(node)
        return False

    def expandAStar(self, node):
        # add nodes to fringe here
        pass

    def AStar(self, start):
        self.Visited = set()
        self.calcHeuristic(start)
        node = start
        heapq.heappush(self.fringeAStar,node)
        while self.fringeAStar:
            node = heapq.heappop(self.fringeAStar)
            if self.checkGoal(node):
                return node
            else:
                if node not in self.Visited:
                    self.Visited.add(node)
                    self.expandAStar(node)
        return False


    def expandUCS(self, node):
        lst = []
        return lst

    def ucs(self, start):
        self.Visited = set()
        node = start
        heapq.heappush(self.fringeUCS, node)
        while self.fringeUCS:
            node = heapq.heappop(self.fringeUCS)
            if self.checkGoal(node):
                return node
            else:
                if node not in self.Visited:
                    self.Visited.add(node)
                    self.expandUCS(node)
        return False

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "G"), ("D", "G")]
costs = {("A", "B"): 1, ("A", "C"): 4, ("B", "D"): 2, ("C", "D"): 1, ("D", "E"): 5, ("E", "G"): 2, ("D", "G"): 1}
g = Graph(edges, costs,["G"])

bfsPath = g.bfs("A")
dfsPath = g.dfs("A")
print("BFS Path: ", bfsPath)
print("DFS Path: ", dfsPath)

