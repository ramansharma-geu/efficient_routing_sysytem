from lsdb import LSDB
from collections import defaultdict
import heapq

class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.networkLSA = LSDB()

    def receive_lsa(self, lsa):
        self.networkLSA.add_router_lsa(lsa)

    def advertise_database(self):
        return self.networkLSA.advertise_database()

    def update_database(self, lsas):
        self.networkLSA.update_database(lsas)

    def neighbors(self):
        return self.networkLSA.neighbors(self.router_id)

    def adjacent(self, other_router):
        same = self.networkLSA.advertise_database() == other_router.advertise_database()
        if not same:
            if self.router_id < other_router.router_id:
                print(f"[DEBUG] LSDB mismatch: Router {self.router_id} vs {other_router.router_id}")
        return same

    def calculate_dijkstras(self):
        graph = defaultdict(list)
        for src in self.networkLSA.get_all_destinations():
            for dest, cost in self.networkLSA.find_connections_with(src):
                graph[src].append((dest, cost))

        self.distances = {}
        self.previous = {}

        pq = [(0, self.router_id)]
        visited = set()

        while pq:
            cost, node = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            self.distances[node] = cost

            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor))
                    if neighbor not in self.previous or cost + weight < self.distances.get(neighbor, float("inf")):
                        self.previous[neighbor] = node

    def generate_forwarding_table(self):
        table = []
        for dest in self.networkLSA.get_all_destinations():
            if dest == self.router_id or dest not in self.distances:
                continue

            next_hop = dest
            while self.previous.get(next_hop) != self.router_id:
                next_hop = self.previous.get(next_hop)
                if next_hop is None:
                    break

            if next_hop is not None:
                table.append((dest, next_hop, self.distances[dest]))

        return sorted(table, key=lambda x: x[0])
    
    def add_link(self, other_router, cost=1):
     if not hasattr(self, 'links'):
        self.links = {}
     self.links[other_router.router_id] = cost