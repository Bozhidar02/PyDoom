from collections import deque


class Pathfinder:
    def __init__(self, game):
        self.visited = None
        self.game = game
        self.map = game.map.game_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, dest):
        self.visited = self.bfs(start, dest, self.graph)
        path = [dest]
        step = self.visited.get(dest, start)
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, dest, graph):
        queue = deque([start])
        visited = {start: None}
        while queue:
            node = queue.popleft()
            if node == dest:
                break
            for next_node in graph[node]:
                if next_node not in visited and next_node not in self.game.object_manager.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = node
        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
