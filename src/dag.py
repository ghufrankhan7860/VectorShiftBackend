from collections import defaultdict, deque

class DAG:
    def __init__(self, nodes, edges):
        self.graph = defaultdict(list)
        self.in_degree = {node: 0 for node in nodes}
        
        for src, dst in edges:
            self.graph[src].append(dst)
            self.in_degree[dst] += 1

    def topological_sort(self):
        # Kahn's Algorithm
        queue = deque([node for node in self.in_degree if self.in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in self.graph[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.in_degree):
            raise ValueError("Graph contains a cycle!")
        return result

    def has_cycle(self):
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.in_degree:
            if node not in visited:
                if dfs(node):
                    return True
        return False
