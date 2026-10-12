
"""Final integrated, reproducible smart traffic demonstration."""
import heapq
import itertools
import math

from graph import graph, coordinates
from traffic_csp import (
    DEMAND, CYCLE, CLEARANCE, MIN_GREEN,
    solve_junction, validate_schedules,
)
from congestion import expected_travel_time


# Synthetic mapping for demonstrating signal effects on campus routes.
# Replace these mappings with measured junction locations in a real network.
NODE_JUNCTION = {
    "Girls Hostel": "J1",
    "Food Court": "J2",
    "Sports Complex": "J3",
    "Parking": "J4",
}


def heuristic_scale(road_graph, coords):
    """Largest globally safe scale for the Euclidean distance heuristic."""
    ratios = []
    for source, neighbours in road_graph.items():
        for target, weight in neighbours.items():
            if weight < 0:
                raise ValueError("A* requires non-negative edge costs")
            distance = math.dist(coords[source], coords[target])
            if distance > 0:
                ratios.append(weight / distance)
    return min(ratios, default=0.0)


def astar_safe(road_graph, coords, start, goal):
    """A* with a graph-scaled Euclidean heuristic and path-cost result."""
    if start not in road_graph or goal not in road_graph:
        raise ValueError("Unknown start or goal")

    scale = heuristic_scale(road_graph, coords)

    def h(node):
        return scale * math.dist(coords[node], coords[goal])

    counter = itertools.count()
    queue = [(h(start), next(counter), 0.0, start, [start])]
    best = {start: 0.0}
    trace = []

    while queue:
        f, _, g, node, path = heapq.heappop(queue)
        if g > best.get(node, float("inf")):
            continue

        trace.append((node, g, h(node), g + h(node)))

        if node == goal:
            return path, g, trace

        for nxt, weight in road_graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("A* requires non-negative edge costs")
            candidate = g + weight
            if candidate < best.get(nxt, float("inf")):
                best[nxt] = candidate
                heapq.heappush(
                    queue,
                    (candidate + h(nxt), next(counter),
                     candidate, nxt, path + [nxt])
                )

    return [], float("inf"), trace


def dijkstra(road_graph, start, goal):
    """Independent shortest-path reference for optimality checks."""
    queue = [(0.0, start, [start])]
    best = {start: 0.0}

    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost > best.get(node, float("inf")):
            continue
        if node == goal:
            return path, cost

        for nxt, weight in road_graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("Negative edge cost")
            candidate = cost + weight
            if candidate < best.get(nxt, float("inf")):
                best[nxt] = candidate
                heapq.heappush(queue, (candidate, nxt, path + [nxt]))

    return [], float("inf")


def expected_cost_route(road_graph, start, goal, scenarios=None,
                        forbidden_nodes=(), blocked_edges=()):
    """Find a minimum expected-cost route using Dijkstra."""
    scenarios = scenarios or {}
    forbidden_nodes = set(forbidden_nodes)
    blocked_edges = set(blocked_edges)

    queue = [(0.0, start, [start])]
    best = {start: 0.0}

    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost > best.get(node, float("inf")):
            continue
        if node == goal:
            return path, cost

        for nxt, base_cost in road_graph.get(node, {}).items():
            if (node, nxt) in blocked_edges:
                continue
            if nxt in forbidden_nodes and nxt != goal:
                continue

            edge_cost = (
                expected_travel_time(scenarios[(node, nxt)])
                if (node, nxt) in scenarios else base_cost
            )
            if edge_cost < 0:
                raise ValueError("Negative expected edge cost")

            candidate = cost + edge_cost
            if candidate < best.get(nxt, float("inf")):
                best[nxt] = candidate
                heapq.heappush(
                    queue, (candidate, nxt, path + [nxt])
                )

    return [], float("inf")


def schedules_for(optimized):
    if optimized:
        result = {j: solve_junction(d) for j, d in DEMAND.items()}
    else:
        result = {
            j: {
                "NS": 40, "EW": 40,
                "clearance": CLEARANCE, "cycle": CYCLE,
            }
            for j in DEMAND
        }

    validate_schedules(result)

    # The two phases are mutually exclusive. Their minimum green is
    # used as a pedestrian-service proxy; separate pedestrian phases
    # would require explicit pedestrian variables and crossing data.
    for junction, signal in result.items():
        assert signal["NS"] >= MIN_GREEN
        assert signal["EW"] >= MIN_GREEN
        assert signal["NS"] + signal["EW"] + signal["clearance"] == CYCLE

    return result


def average_phase_wait(signal, demand):
    """Expected red wait under uniform arrivals, demand-weighted by phase."""
    cycle = signal["cycle"]
    numerator = 0.0
    total_demand = 0.0

    for phase in ("NS", "EW"):
        green = signal[phase]
        wait = (cycle - green) ** 2 / (2.0 * cycle)
        numerator += demand[phase] * wait
        total_demand += demand[phase]

    return numerator / total_demand if total_demand else 0.0


def simulate_average_trip_cost(trips, schedules):
    """Illustrative network simulation using a synthetic node-junction map."""
    results = []

    for start, goal in trips:
        path, road_cost, _ = astar_safe(graph, coordinates, start, goal)
        if not path:
            raise RuntimeError(f"No route: {start} -> {goal}")

        total = road_cost
        for node in path[1:-1]:
            junction = NODE_JUNCTION.get(node)
            if junction is not None:
                total += average_phase_wait(
                    schedules[junction], DEMAND[junction]
                )
        results.append(total)

    return sum(results) / len(results)


def emergency_priority_plan(route, schedules):
    """Return a simulated priority request, preserving cycle constraints."""
    if len(route) < 2:
        raise ValueError("Emergency route must contain at least two nodes")

    requests = []
    for node in route:
        junction = NODE_JUNCTION.get(node)
        if junction:
            # Request priority for the approach with higher demand.
            phase = max(DEMAND[junction], key=DEMAND[junction].get)
            requests.append({
                "junction": junction,
                "requested_phase": phase,
                "reason": "Emergency corridor priority request",
            })

    return {
        "route": list(route),
        "priority_requests": requests,
        "base_schedules": schedules,
        "simulation_only": True,
    }


def main():
    start, goal = "Boys Hostel", "Main Gate"

    print("=" * 60)
    print("FINAL SMART TRAFFIC MANAGEMENT DEMONSTRATION")
    print("=" * 60)

    path, cost, trace = astar_safe(graph, coordinates, start, goal)
    _, reference_cost = dijkstra(graph, start, goal)

    print("\n1. A* WITH ADMISSIBLE SCALED EUCLIDEAN HEURISTIC")
    for node, g, h, f in trace:
        print(f"{node}: g={g:.2f}, h={h:.2f}, f={f:.2f}")
    print("Route:", " -> ".join(path))
    print(f"A* cost: {cost:.2f}; Dijkstra cost: {reference_cost:.2f}")
    print("Optimality verified:", math.isclose(cost, reference_cost))

    from incident_rules import IncidentManager
    manager = IncidentManager(graph)
    manager.accident("Boys Hostel", "Food Court")
    updated = manager.get_updated_graph()
    new_path, new_cost, _ = astar_safe(updated, coordinates, start, goal)
    _, dynamic_reference = dijkstra(updated, start, goal)

    print("\n2. DYNAMIC GRAPH AFTER ACCIDENT")
    print("Route:", " -> ".join(new_path))
    print(f"A* cost: {new_cost:.2f}; Dijkstra cost: {dynamic_reference:.2f}")
    print("Dynamic optimality verified:",
          math.isclose(new_cost, dynamic_reference))

    scenarios = {
        ("Boys Hostel", "Food Court"): [(0.5, 4.5), (0.5, 20.0)],
        ("Boys Hostel", "Girls Hostel"): [(0.8, 2.3), (0.2, 5.0)],
    }
    fair_path, fair_cost = expected_cost_route(
        graph, start, goal, scenarios,
        forbidden_nodes={"Food Court"},
    )
    print("\n3. EXPECTED-COST ROUTING WITH RESTRICTED ZONE")
    print("Illustrative restricted node: Food Court")
    print("Route:", " -> ".join(fair_path))
    print(f"Expected cost: {fair_cost:.2f}")

    baseline_schedules = schedules_for(False)
    optimized_schedules = schedules_for(True)

    print("\n4. CSP SIGNAL SCHEDULES")
    for junction, signal in optimized_schedules.items():
        print(junction, signal)
    print("Cycle, clearance, minimum-green and exclusive-phase checks passed.")

    emergency = emergency_priority_plan(
        ["Boys Hostel", "Girls Hostel", "Food Court", "Parking"],
        optimized_schedules,
    )
    print("\n5. EMERGENCY PRIORITY REQUEST")
    print(emergency["priority_requests"])
    print("This creates a simulated request; it does not control real signals.")

    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]
    before = simulate_average_trip_cost(trips, baseline_schedules)
    after = simulate_average_trip_cost(trips, optimized_schedules)

    print("\n6. BEFORE/AFTER SIMULATED TRIP COST")
    print(f"Baseline mean cost: {before:.2f}")
    print(f"CSP mean cost: {after:.2f}")
    print(f"Estimated reduction: {(before-after)/before*100:.2f}%")
    print("Synthetic estimate only; validate the junction mapping and time units.")

    print("\n7. PRIVACY AND GOVERNANCE")
    print("- Collect GPS only with consent and for a defined purpose.")
    print("- Minimize location precision, retention and access.")
    print("- Audit routing decisions and assess effects on vulnerable communities.")
    print("- Replace illustrative restricted nodes with verified school/residential metadata.")
    print("- Implement separate pedestrian crossing variables before deployment.")


if __name__ == "__main__":
    main()
