"""Evaluate campus routes and CSP-generated traffic signal timings.

Signal waiting times are theoretical estimates. Junction-to-road
mappings are not yet available, so this does not claim to calculate
real end-to-end campus travel times.
"""

import heapq

from graph import graph
from traffic_csp import DEMAND, solve_junction, validate_schedules


# Existing signal timings before optimization.
JUNCTIONS = {
    "J1": {"NS": 53, "EW": 27, "clearance": 10, "cycle": 90},
    "J2": {"NS": 23, "EW": 57, "clearance": 10, "cycle": 90},
    "J3": {"NS": 47, "EW": 33, "clearance": 10, "cycle": 90},
    "J4": {"NS": 17, "EW": 63, "clearance": 10, "cycle": 90},
}
ORIGINAL_SCHEDULES = JUNCTIONS

def shortest_path(road_graph, start, goal, edge_cost):
    """Dijkstra search using a supplied nonnegative edge-cost function."""
    queue = [(0.0, start)]
    distances = {start: 0.0}
    previous = {}

    while queue:
        cost, node = heapq.heappop(queue)

        if cost > distances[node]:
            continue

        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            path.reverse()
            return path, cost

        for neighbour, weight in road_graph[node].items():
            adjusted = edge_cost(node, neighbour, weight)

            if adjusted < 0:
                raise ValueError("Negative edge cost")

            candidate = cost + adjusted

            if candidate < distances.get(neighbour, float("inf")):
                distances[neighbour] = candidate
                previous[neighbour] = node
                heapq.heappush(queue, (candidate, neighbour))

    return None, float("inf")


def validate_schedules(schedules=None):
    if schedules is None:
        schedules = JUNCTIONS

    for junction, signal in schedules.items():
        assert signal["NS"] >= 15, f"{junction}: NS phase too short"
        assert signal["EW"] >= 15, f"{junction}: EW phase too short"
        assert (
            signal["NS"] + signal["EW"] + signal["clearance"]
            == signal["cycle"]
        ), f"{junction}: cycle length mismatch"

def average_wait(green, cycle):
    """Expected red-light wait for uniform arrivals at a fixed signal.

    Assumes a simple periodic signal with one continuous green phase.
    This is an approximation, not a measured traffic delay.
    """
    red = cycle - green
    return red * red / (2.0 * cycle)


def simulate_signal_wait(schedules, movements):
    """Sum expected signal waits for the specified simulated movements.

    Each movement is (junction, phase, traversal_count).
    """
    total_wait = 0.0

    for junction, phase, count in movements:
        signal = schedules[junction]
        total_wait += count * average_wait(
            signal[phase], signal["cycle"]
        )

    return total_wait


def main():
    validate_schedules()

    # Use the actual CSP solver rather than manually chosen timings.
    optimized_schedules = {
        junction: solve_junction(demand)
        for junction, demand in DEMAND.items()
    }
    validate_schedules(optimized_schedules)

    print("SMART TRAFFIC MANAGEMENT - EVALUATION")
    print("=" * 50)
    print("Original and CSP-generated schedules validated.")

    print("\nCSP-generated signal schedules:")
    for junction, signal in optimized_schedules.items():
        print(
            f"{junction}: NS={signal['NS']}s, "
            f"EW={signal['EW']}s, "
            f"clearance={signal['clearance']}s, "
            f"cycle={signal['cycle']}s"
        )

    # Illustrative movement scenario.
    # These counts are simulation assumptions, not observed traffic.
    movements = [
        ("J1", "NS", 1),
        ("J2", "EW", 1),
        ("J3", "NS", 1),
        ("J4", "EW", 1),
    ]

    before_wait = simulate_signal_wait(
        ORIGINAL_SCHEDULES, movements
    )
    after_wait = simulate_signal_wait(
        optimized_schedules, movements
    )

    print("\nIllustrative signal-wait comparison:")
    print(f"Before: {before_wait:.2f} seconds")
    print(f"After:  {after_wait:.2f} seconds")

    if before_wait > 0:
        reduction = (before_wait - after_wait) / before_wait * 100
        print(f"Estimated wait reduction: {reduction:.2f}%")

    print("\nBaseline campus route:")
    path, cost = shortest_path(
        graph,
        "Boys Hostel",
        "Main Gate",
        lambda u, v, weight: weight,
    )

    print("Path:", path)
    print(f"Graph cost: {cost:.2f}")

    print("\nLimitations:")
    print("- Movement counts are illustrative.")
    print("- Junctions are not yet mapped to road edges.")
    print("- Graph weights have not been confirmed as seconds.")
    print("- Signal waits are estimates, not measured delays.")
    print("- The CSP solution is demand-proportional, not proven")
    print("  to minimize actual network travel time.")


if __name__ == "__main__":
    main()
