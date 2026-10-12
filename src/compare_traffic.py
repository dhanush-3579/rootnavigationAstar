"""Reproducible simulated travel-time comparison."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import graph
from incident_rules import IncidentManager
from dynamic_routing import astar_route


def average_route_time(road_graph, trips):
    times = []
    for start, goal in trips:
        path, cost = astar_route(road_graph, start, goal)
        if not path:
            raise RuntimeError(f"No route from {start} to {goal}")
        times.append(cost)
    return sum(times) / len(times)


def main():
    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]

    baseline = average_route_time(graph, trips)

    manager = IncidentManager(graph)
    manager.set_weather(rain=True, night=True)
    optimized_graph = manager.get_updated_graph()

    optimized = average_route_time(optimized_graph, trips)
    improvement = (baseline - optimized) / baseline * 100

    print("SIMULATED ROUTE TRAVEL-TIME COMPARISON")
    print(f"Trips evaluated: {len(trips)}")
    print(f"Baseline average cost: {baseline:.2f}")
    print(f"Updated average cost:  {optimized:.2f}")
    print(f"Change: {improvement:.2f}%")
    print("Note: These are illustrative graph costs, not validated real-world times.")


if __name__ == "__main__":
    main()
