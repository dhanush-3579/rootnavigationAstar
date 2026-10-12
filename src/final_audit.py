
"""Final audit: optimized signal timing, routing checks and honest reporting."""
import math

from graph import graph, coordinates
from traffic_csp import DEMAND, CYCLE, CLEARANCE, MIN_GREEN
from final_completion import astar_safe, dijkstra
from final_remaining import shortest_route, protected_nodes


MIN_PEDESTRIAN = 10
NODE_JUNCTION = {
    "Girls Hostel": "J1",
    "Food Court": "J2",
    "Sports Complex": "J3",
    "Parking": "J4",
}


def phase_wait(cycle, green):
    # Expected red-light waiting time for uniform arrivals.
    return (cycle - green) ** 2 / (2 * cycle)


def optimize_junction(demand):
    """Exhaustively choose feasible NS/EW green splits with pedestrian time."""
    available = CYCLE - CLEARANCE - MIN_PEDESTRIAN
    best = None

    for ns in range(MIN_GREEN, available - MIN_GREEN + 1):
        ew = available - ns
        if ew < MIN_GREEN:
            continue

        # Minimize demand-weighted expected signal waiting cost.
        objective = (
            demand["NS"] * phase_wait(CYCLE, ns)
            + demand["EW"] * phase_wait(CYCLE, ew)
        )
        candidate = {
            "NS": ns,
            "EW": ew,
            "pedestrian": MIN_PEDESTRIAN,
            "clearance": CLEARANCE,
            "cycle": CYCLE,
        }
        if best is None or objective < best[0]:
            best = (objective, candidate)

    if best is None:
        raise RuntimeError("No feasible junction schedule")
    return best[1]


def optimize_all():
    return {j: optimize_junction(d) for j, d in DEMAND.items()}


def validate(schedules):
    for junction, s in schedules.items():
        assert s["NS"] >= MIN_GREEN
        assert s["EW"] >= MIN_GREEN
        assert s["pedestrian"] >= MIN_PEDESTRIAN
        assert s["NS"] + s["EW"] + s["pedestrian"] + s["clearance"] == CYCLE


def evaluate(trips, schedules):
    """Synthetic road cost plus demand-weighted signal waiting at mapped nodes."""
    total = 0.0

    for start, goal in trips:
        path, road_cost, _ = astar_safe(
            graph, coordinates, start, goal
        )
        if not path:
            raise RuntimeError(f"No route from {start} to {goal}")

        trip_cost = road_cost
        for node in path[1:-1]:
            junction = NODE_JUNCTION.get(node)
            if junction is None:
                continue

            signal = schedules[junction]
            demand = DEMAND[junction]
            total_demand = demand["NS"] + demand["EW"]
            weighted_wait = (
                demand["NS"] * phase_wait(CYCLE, signal["NS"])
                + demand["EW"] * phase_wait(CYCLE, signal["EW"])
            ) / total_demand
            trip_cost += weighted_wait

        total += trip_cost

    return total / len(trips)


def main():
    start, goal = "Boys Hostel", "Main Gate"
    a_path, a_cost, _ = astar_safe(graph, coordinates, start, goal)
    d_path, d_cost = dijkstra(graph, start, goal)

    print("1. A* OPTIMALITY AUDIT")
    print("A*:", " -> ".join(a_path), f"cost={a_cost:.2f}")
    print("Dijkstra:", " -> ".join(d_path), f"cost={d_cost:.2f}")
    print("Costs match:", math.isclose(a_cost, d_cost, rel_tol=1e-9))

    optimized = optimize_all()
    validate(optimized)
    baseline = {
        j: {
            "NS": 35, "EW": 35, "pedestrian": MIN_PEDESTRIAN,
            "clearance": CLEARANCE, "cycle": CYCLE,
        }
        for j in DEMAND
    }

    print("\n2. DEMAND-WEIGHTED CSP OPTIMIZATION")
    for junction, schedule in optimized.items():
        print(junction, schedule)
    print("All cycles, phase minimums and pedestrian times validated.")

    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]
    before = evaluate(trips, baseline)
    after = evaluate(trips, optimized)

    print("\n3. SYNTHETIC BEFORE/AFTER EVALUATION")
    print(f"Baseline mean cost: {before:.2f}")
    print(f"Optimized mean cost: {after:.2f}")
    print(f"Reduction: {(before-after)/before*100:.2f}%")
    print("Illustrative model only; not calibrated real-world travel time.")

    print("\n4. SCHOOL/RESIDENTIAL ZONES")
    zones = protected_nodes()
    print("Configured protected nodes:", sorted(zones))
    zone_path, zone_cost = shortest_route(
        graph, start, goal, forbidden=zones
    )
    print("Permitted route:", " -> ".join(zone_path) if zone_path else "No route")
    if not zones:
        print("NOT CONFIGURED: add verified node names to src/zone_metadata.json.")

    print("\n5. RESPONSIBLE DEPLOYMENT")
    print("- Emergency priority remains a simulation, not hardware control.")
    print("- Verify school/residential node metadata before claiming zone avoidance.")
    print("- Validate pedestrian timings and signal conflict geometry with engineers.")
    print("- Use consent, GPS minimization, retention limits and decision audits.")


if __name__ == "__main__":
    main()
