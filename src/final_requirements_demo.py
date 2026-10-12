
"""Run the remaining project demonstrations."""
from graph import graph
from incident_rules import IncidentManager
from project_extension import (
    dijkstra, route_with_expected_cost, signal_plan,
    emergency_signal_plan, simulate_signal_cost
)

def main():
    start, goal = "Boys Hostel", "Main Gate"
    path, cost = dijkstra(graph, start, goal)
    print("1. OPTIMALITY BASELINE (DIJKSTRA)")
    print("Path:", " -> ".join(path), "| total cost:", round(cost, 2))

    manager = IncidentManager(graph)
    manager.accident("Boys Hostel", "Food Court")
    dynamic = manager.get_updated_graph()
    dynamic_path, dynamic_cost = dijkstra(dynamic, start, goal)
    print("\n2. DYNAMIC GRAPH REPLAN")
    print("Path:", " -> ".join(dynamic_path), "| total cost:", round(dynamic_cost, 2))

    scenarios = {
        ("Boys Hostel", "Food Court"): [(0.5, 4.5), (0.5, 20.0)],
        ("Boys Hostel", "Girls Hostel"): [(0.8, 2.3), (0.2, 5.0)],
    }
    expected_path, expected_cost = route_with_expected_cost(
        graph, start, goal, scenarios, forbidden={"Food Court"}
    )
    print("\n3. EXPECTED-COST FAIR ROUTING")
    print("Avoided zone: Food Court (illustrative restricted-zone assumption)")
    print("Path:", " -> ".join(expected_path), "| expected cost:", round(expected_cost, 2))

    schedules = signal_plan()
    print("\n4. CSP SIGNAL SCHEDULE")
    for junction, signal in schedules.items():
        print(junction, signal)

    emergency = emergency_signal_plan(
        ["Boys Hostel", "Girls Hostel", "Food Court"], schedules
    )
    print("\n5. EMERGENCY CORRIDOR")
    print(emergency)
    print("Note: this creates a priority plan; it does not control physical signals.")

    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]
    baseline = simulate_signal_cost(graph, trips, {})
    optimized = simulate_signal_cost(graph, trips, schedules)
    print("\n6. SYNTHETIC BEFORE/AFTER SIGNAL SIMULATION")
    print("Baseline mean cost:", round(baseline, 2))
    print("CSP mean cost:", round(optimized, 2))
    if baseline:
        print("Percent change:", round((baseline - optimized) / baseline * 100, 2), "%")
    print("Caution: graph has no junction mapping; this simulation may show no difference.")
    print("\n7. PRIVACY AND GOVERNANCE")
    print("- Collect GPS only with informed consent and only when necessary.")
    print("- Minimize precision, retention, access, and sharing; document deletion.")
    print("- Audit route recommendations and review impacts on vulnerable areas.")
    print("- Zone avoidance is only active when real zone metadata is supplied.")
    print("\nDONE")

if __name__ == "__main__":
    main()
