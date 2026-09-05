# astar.py

import math
import heapq
from collections import deque

from graph import graph, coordinates


# Calculate straight-line distance
def euclidean_heuristic(node, goal):
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# A* Search
def a_star(start, goal):
    priority_queue = []

    # Starting node
    g = 0
    h = euclidean_heuristic(start, goal)
    f = g + h

    heapq.heappush(priority_queue, (f, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    nodes_expanded = 0

    print("\n--- A* Evaluation: f = g + h ---")

    while priority_queue:

        current_f, current = heapq.heappop(priority_queue)

        # Calculate g, h and f
        g = cost_so_far[current]
        h = euclidean_heuristic(current, goal)
        f = g + h

        nodes_expanded += 1

        print(
            f"Node: {current} | "
            f"g = {g:.2f} | "
            f"h = {h:.2f} | "
            f"f = {f:.2f}"
        )

        # Goal reached
        if current == goal:
            break

        # Check neighbouring locations
        for neighbour, distance in graph[current].items():

            new_cost = cost_so_far[current] + distance

            if neighbour not in cost_so_far:
                better_path = True
            else:
                better_path = new_cost < cost_so_far[neighbour]

            if better_path:

                cost_so_far[neighbour] = new_cost

                heuristic = euclidean_heuristic(neighbour, goal)

                priority = new_cost + heuristic

                heapq.heappush(
                    priority_queue,
                    (priority, neighbour)
                )

                came_from[neighbour] = current

    # If destination cannot be reached
    if goal not in came_from:
        return None, float("inf"), nodes_expanded

    # Construct final path
    path = []

    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path, cost_so_far[goal], nodes_expanded


# BFS Search
def bfs(start, goal):

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

    # If destination cannot be reached
    if goal not in came_from:
        return None, float("inf"), nodes_expanded

    # Construct final path
    path = []

    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path, len(path) - 1, nodes_expanded