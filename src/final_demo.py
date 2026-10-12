import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import graph
from astar import a_star
from incident_rules import IncidentManager
from dynamic_routing import astar_route
from traffic_csp import DEMAND, solve_junction, validate_schedules
from congestion import expected_travel_time


def main():
    start, goal = "Boys Hostel", "Main Gate"

    print("=" * 65)
    print("SMART TRAFFIC MANAGEMENT SYSTEM - FINAL DEMO")
    print("=" * 65)

    # 1. Static A* route
    print("\n1. ORIGINAL A* ROUTE")
    result = a_star(start, goal)
    print("Original A* result:", result)

    # 2. Accident and dynamic rerouting
    print("\n2. INCIDENT RULES AND DYNAMIC REROUTING")
    manager = IncidentManager(graph)
    old_path, old_cost = astar_route(graph, start, goal)
    print("Before accident:", " -> ".join(old_path), "| cost:", old_cost)

    manager.accident("Boys Hostel", "Food Court")
    manager.set_weather(rain=True, night=True)
    updated = manager.get_updated_graph()
    new_path, new_cost = astar_route(updated, start, goal)

    print("After accident/weather:", " -> ".join(new_path), "| cost:", new_cost)
    print("Accident edge excluded:", ("Boys Hostel", "Food Court") not in list(zip(new_path, new_path[1:])))

    # 3. Emergency corridor rule
    print("\n3. EMERGENCY VEHICLE")
    emergency_route = ["Boys Hostel", "Girls Hostel", "Food Court"]
    manager.emergency_vehicle(emergency_route)
    print("Recorded emergency corridor:", " -> ".join(manager.emergency_corridor))
    print("Note: recording priority is implemented; automatic signal override requires integration.")

    # 4. CSP signal plan
    print("\n4. CSP SIGNAL SCHEDULE")
    schedules = {j: solve_junction(d) for j, d in DEMAND.items()}
    validate_schedules(schedules)
    for junction, signal in schedules.items():
        print(junction, signal)
    print("All generated schedules passed the solver's validation.")

    # 5. Probabilistic travel time
    print("\n5. PROBABILISTIC CONGESTION")
    scenarios = [(0.6, 7.0), (0.4, 12.0)]
    print("Scenario probabilities/times:", scenarios)
    print("Expected travel time:", expected_travel_time(scenarios))

    # 6. Route cost comparison
    print("\n6. ROUTE COST COMPARISON")
    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]
    before = [astar_route(graph, a, b)[1] for a, b in trips]
    after = [astar_route(updated, a, b)[1] for a, b in trips]
    avg_before = sum(before) / len(before)
    avg_after = sum(after) / len(after)
    print(f"Baseline average graph cost: {avg_before:.2f}")
    print(f"Incident/weather average graph cost: {avg_after:.2f}")
    print("These are simulated graph costs, not measured real-world travel times.")

    print("\n7. RESPONSIBLE AI CHECKLIST")
    print("- Avoid school/residential zones using explicit graph metadata and route constraints.")
    print("- Minimize GPS collection; obtain consent and define retention/access controls.")
    print("- Log routing decisions and incident changes for auditing.")
    print("- Re-plan after graph updates and compare A* with Dijkstra for optimality.")
    print("- Current graph has no school/residential metadata or calibrated time units.")
    print("\nDEMO FINISHED")


if __name__ == "__main__":
    main()
