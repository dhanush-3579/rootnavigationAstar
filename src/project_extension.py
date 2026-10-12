
"""Integrated demonstration helpers for the Smart Traffic project."""
import heapq
import itertools
from traffic_csp import DEMAND, solve_junction, validate_schedules
from congestion import expected_travel_time


def dijkstra(graph, start, goal):
    queue = [(0.0, start, [start])]
    best = {start: 0.0}
    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost != best.get(node):
            continue
        if node == goal:
            return path, cost
        for nxt, weight in graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("Negative edge costs are unsupported")
            new = cost + weight
            if new < best.get(nxt, float("inf")):
                best[nxt] = new
                heapq.heappush(queue, (new, nxt, path + [nxt]))
    return [], float("inf")


def expected_edge_cost(scenarios):
    """Expected cost for each directed edge: edge -> [(probability, cost)]."""
    return {edge: expected_travel_time(values) for edge, values in scenarios.items()}


def route_with_expected_cost(graph, start, goal, edge_scenarios=None, forbidden=()):
    """Dijkstra on expected edge costs; forbidden nodes implement zone avoidance."""
    costs = expected_edge_cost(edge_scenarios or {})
    blocked_nodes = set(forbidden)
    queue = [(0.0, start, [start])]
    best = {start: 0.0}
    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost != best.get(node):
            continue
        if node == goal:
            return path, cost
        for nxt, base in graph.get(node, {}).items():
            if nxt in blocked_nodes and nxt != goal:
                continue
            weight = costs.get((node, nxt), base)
            new = cost + weight
            if new < best.get(nxt, float("inf")):
                best[nxt] = new
                heapq.heappush(queue, (new, nxt, path + [nxt]))
    return [], float("inf")


def signal_plan():
    schedules = {j: solve_junction(d) for j, d in DEMAND.items()}
    validate_schedules(schedules)
    return schedules


def emergency_signal_plan(route, schedules):
    """Illustrative priority plan: validate route and record junction corridor."""
    if len(route) < 2:
        raise ValueError("Emergency route must contain at least two nodes")
    return {"route": list(route), "priority": True, "schedules": schedules}


def simulate_signal_cost(graph, trips, schedules):
    """Synthetic delay model; graph nodes are assumed to be junctions for demo only."""
    total = 0.0
    for start, goal in trips:
        path, road_cost = dijkstra(graph, start, goal)
        if not path:
            raise RuntimeError(f"No route {start} -> {goal}")
        delay = 0.0
        for node in path[1:-1]:
            signal = schedules.get(node)
            if signal:
                cycle = signal["cycle"]
                green = max(signal["NS"], signal["EW"])
                delay += (cycle - green) ** 2 / (2 * cycle)
        total += road_cost + delay
    return total / len(trips)
