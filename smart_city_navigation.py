import heapq

class Graph:
    def __init__(self):
        self.adj = {}

    def add_junction(self, name):
        if name not in self.adj:
            self.adj[name] = []

    def add_road(self, u, v, distance):
        self.add_junction(u)
        self.add_junction(v)
        self.adj[u].append((v, distance))
        self.adj[v].append((u, distance))

    def display(self):
        if not self.adj:
            print("No roads defined yet.")
            return
        print("\n--- Road Network (Adjacency List) ---")
        for node, neighbours in self.adj.items():
            edges = ", ".join(f"{nbr}({dist})" for nbr, dist in neighbours)
            print(f"{node} -> {edges}")
        print()

    def bfs(self, start):
        if start not in self.adj:
            print("Start junction not found.")
            return
        visited = set()
        queue = [start]
        visited.add(start)
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for nbr, _ in self.adj[node]:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)
        print("BFS traversal order:", " -> ".join(order))

    def dfs(self, start):
        if start not in self.adj:
            print("Start junction not found.")
            return
        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)
            for nbr, _ in self.adj[node]:
                if nbr not in visited:
                    _dfs(nbr)

        _dfs(start)
        print("DFS traversal order:", " -> ".join(order))

    def dijkstra(self, start, end):
        if start not in self.adj or end not in self.adj:
            print("Start or destination junction not found.")
            return
        dist = {node: float('inf') for node in self.adj}
        prev = {node: None for node in self.adj}
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            current_dist, node = heapq.heappop(heap)
            if current_dist > dist[node]:
                continue
            if node == end:
                break
            for nbr, w in self.adj[node]:
                nd = current_dist + w
                if nd < dist[nbr]:
                    dist[nbr] = nd
                    prev[nbr] = node
                    heapq.heappush(heap, (nd, nbr))

        if dist[end] == float('inf'):
            print("No path found between the given junctions.")
            return

        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        print("Shortest path:", " -> ".join(path))
        print("Total distance:", dist[end])


class ZoneNode:
    def __init__(self, name):
        self.name = name
        self.children = []


class ZoneTree:
    def __init__(self):
        self.root = None

    def set_root(self, name):
        if self.root is None:
            self.root = ZoneNode(name)
        else:
            self.root.name = name

    def _find(self, node, name):
        if node is None:
            return None
        if node.name == name:
            return node
        for child in node.children:
            res = self._find(child, name)
            if res:
                return res
        return None

    def add_zone(self, parent_name, zone_name):
        if self.root is None:
            print("Create a root zone first.")
            return
        parent_node = self._find(self.root, parent_name)
        if not parent_node:
            print("Parent zone not found.")
            return
        parent_node.children.append(ZoneNode(zone_name))

    def _display(self, node, level):
        if node is None:
            return
        print("  " * level + "- " + node.name)
        for child in node.children:
            self._display(child, level + 1)

    def display(self):
        if self.root is None:
            print("No zones defined yet.")
            return
        print("\n--- City Zone Hierarchy ---")
        self._display(self.root, 0)
        print()


def read_float(prompt, minimum=None):
    while True:
        try:
            val = float(input(prompt))
            if minimum is not None and val < minimum:
                print(f"Value must be >= {minimum}")
                continue
            return val
        except ValueError:
            print("Invalid number. Try again.")


def main():
    graph = Graph()
    zones = ZoneTree()

    while True:
        print("\n====== SMART CITY ROAD NAVIGATION SYSTEM ======")
        print("1. Add Junction")
        print("2. Add Road")
        print("3. Display Road Map")
        print("4. Shortest Path (Dijkstra)")
        print("5. BFS Traversal")
        print("6. DFS Traversal")
        print("7. Manage City Zones")
        print("8. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            name = input("Enter junction name: ").strip()
            graph.add_junction(name)
            print("Junction added.")
        elif choice == "2":
            u = input("From junction: ").strip()
            v = input("To junction: ").strip()
            d = read_float("Distance / cost: ", minimum=0)
            graph.add_road(u, v, d)
            print("Road added.")
        elif choice == "3":
            graph.display()
        elif choice == "4":
            start = input("Start junction: ").strip()
            end = input("Destination junction: ").strip()
            graph.dijkstra(start, end)
        elif choice == "5":
            start = input("Start junction for BFS: ").strip()
            graph.bfs(start)
        elif choice == "6":
            start = input("Start junction for DFS: ").strip()
            graph.dfs(start)
        elif choice == "7":
            while True:
                print("\n--- City Zone Management ---")
                print("1. Set / Change Root Zone")
                print("2. Add Child Zone")
                print("3. Display Zone Hierarchy")
                print("4. Back to Main Menu")
                sub = input("Select option: ").strip()
                if sub == "1":
                    name = input("Root zone name (e.g., City, State): ").strip()
                    zones.set_root(name)
                    print("Root zone set.")
                elif sub == "2":
                    parent = input("Parent zone name: ").strip()
                    child = input("Child zone name: ").strip()
                    zones.add_zone(parent, child)
                elif sub == "3":
                    zones.display()
                elif sub == "4":
                    break
                else:
                    print("Invalid option.")
        elif choice == "8":
            print("Exiting Smart City Road Navigation System. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
