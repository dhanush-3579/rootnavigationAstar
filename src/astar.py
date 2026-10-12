import heapq
import math
from collections import deque

from graph import graph, coordinates


def euclidean_heuristic(node, goal):
    if node == goal:
        return 0.0

    scale = float("inf")

    for source, neighbours in graph.items():
        for destination, edge_cost in neighbours.items():
            if edge_cost < 0:
                raise ValueError("Edge costs must be non-negative.")

            if source not in coordinates or destination not in coordinates:
                return 0.0

            x1, y1 = coordinates[source]
            x2, y2 = coordinates[destination]
            distance = math.hypot(x1 - x2, y1 - y2)

            if distance > 0:
                scale = min(scale, edge_cost / distance)

    if scale == float("inf"):
        scale = 0.0

    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]

    return scale * math.hypot(x1 - x2, y1 - y2)


def a_star(start, goal):
    if start not in graph or goal not in graph:
        raise KeyError("Invalid start or destination.")

    queue = []
    counter = 0
    came_from = {start: None}
    cost_so_far = {start: 0.0}

    heapq.heappush(
        queue,
        (euclidean_heuristic(start, goal), counter, start)
    )

    nodes_expanded = 0

    print("\n--- A*: f(n) = g(n) + h(n) ---")

    while queue:
        current_f, _, current = heapq.heappop(queue)
        g = cost_so_far[current]
        h = euclidean_heuristic(current, goal)

        if current_f > g + h + 1e-9:
            continue

        nodes_expanded += 1

        print(
            f"{current}: g={g:.2f}, "
            f"h={h:.2f}, f={g + h:.2f}"
        )

        if current == goal:
            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = came_from[node]

            path.reverse()
            return path, g, nodes_expanded

        for neighbour, edge_cost in graph[current].items():
            if edge_cost < 0:
                raise ValueError("Edge costs must be non-negative.")

            new_cost = g + edge_cost

            if new_cost < cost_so_far.get(neighbour, float("inf")):
                cost_so_far[neighbour] = new_cost
                came_from[neighbour] = current
                counter += 1

                h_next = euclidean_heuristic(neighbour, goal)

                heapq.heappush(
                    queue,
                    (new_cost + h_next, counter, neighbour)
                )

    return None, float("inf"), nodes_expanded


def bfs(start, goal):
    if start not in graph or goal not in graph:
        raise KeyError("Invalid start or destination.")

    queue = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        if current == goal:
            break

        for neighbour in graph[current]:
            if neighbour not in came_from:
                came_from[neighbour] = current
                queue.append(neighbour)

    if goal not in came_from:
        return None, float("inf"), nodes_expanded

    path = []
    node = goal

    while node is not None:
        path.append(node)
        node = came_from[node]

    path.reverse()
    return path, len(path) - 1, nodes_expanded