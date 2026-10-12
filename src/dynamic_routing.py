"""A* routing on a supplied, possibly updated road graph."""
import heapq
import itertools


def astar_route(road_graph, start, goal, heuristic=None):
    """Return (path, cost); use h=0 by default to guarantee admissibility."""
    if start not in road_graph or goal not in road_graph:
        raise ValueError("Start and goal must exist in the graph.")

    if heuristic is None:
        heuristic = lambda node, target: 0.0

    counter = itertools.count()
    queue = [(heuristic(start, goal), next(counter), 0.0, start, [start])]
    best_cost = {start: 0.0}

    while queue:
        _, _, cost, node, path = heapq.heappop(queue)

        if cost > best_cost.get(node, float("inf")):
            continue

        if node == goal:
            return path, cost

        for neighbour, weight in road_graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("A* requires non-negative edge costs.")

            new_cost = cost + weight
            if new_cost < best_cost.get(neighbour, float("inf")):
                best_cost[neighbour] = new_cost
                priority = new_cost + heuristic(neighbour, goal)
                heapq.heappush(
                    queue,
                    (priority, next(counter), new_cost,
                     neighbour, path + [neighbour])
                )

    return [], float("inf")
