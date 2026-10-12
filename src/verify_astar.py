"""Compare A* results against Dijkstra for every campus location pair."""

import heapq

from graph import graph
from astar import a_star


def dijkstra(road_graph, start, goal):
    queue = [(0.0, start)]
    distances = {start: 0.0}

    while queue:
        cost, node = heapq.heappop(queue)

        if cost > distances[node]:
            continue

        if node == goal:
            return cost

        for neighbour, weight in road_graph[node].items():
            if weight < 0:
                raise ValueError("Negative edge weight detected.")

            new_cost = cost + weight

            if new_cost < distances.get(neighbour, float("inf")):
                distances[neighbour] = new_cost
                heapq.heappush(queue, (new_cost, neighbour))

    return float("inf")


def main():
    checked = 0

    for start in graph:
        for goal in graph:
            if start == goal:
                continue

            astar_path, astar_cost, _ = a_star(start, goal)
            optimal_cost = dijkstra(graph, start, goal)

            if astar_path is None:
                astar_cost = float("inf")

            if abs(astar_cost - optimal_cost) > 1e-8:
                if astar_cost != optimal_cost:
                    raise AssertionError(
                        f"Mismatch for {start} -> {goal}: "
                        f"A*={astar_cost}, Dijkstra={optimal_cost}"
                    )

            checked += 1

    print("A* optimality verification passed.")
    print("Start/destination pairs checked:", checked)
    print("A* costs matched Dijkstra for every tested pair.")


if __name__ == "__main__":
    main()