
"""Final extension: pedestrian CSP, zone policy, emergency requests and evaluation."""
import heapq
import json
from pathlib import Path

from graph import graph
from traffic_csp import DEMAND, CYCLE, CLEARANCE, MIN_GREEN


MIN_PEDESTRIAN = 10
EMERGENCY_BONUS = 5


def solve_full_csp(demand):
    """Backtracking CSP: NS, EW and pedestrian green share the fixed cycle."""
    available = CYCLE - CLEARANCE
    result = None

    # Most-demanded approach is tried first; pedestrian green is always protected.
    for pedestrian in range(MIN_PEDESTRIAN, available - 2 * MIN_GREEN + 1):
        remaining = available - pedestrian
        ns_values = sorted(
            range(MIN_GREEN, remaining - MIN_GREEN + 1),
            key=lambda x: abs(
                x / remaining -
                demand["NS"] / (demand["NS"] + demand["EW"])
            )
        )
        for ns in ns_values:
            ew = remaining - ns
            if ew < MIN_GREEN:
                continue
            # NS and EW are exclusive phases; they never receive green together.
            result = {
                "NS": ns,
                "EW": ew,
                "pedestrian": pedestrian,
                "clearance": CLEARANCE,
                "cycle": CYCLE,
            }
            break
        if result:
            break

    if result is None:
        raise ValueError("No feasible signal schedule")
    assert sum(result[k] for k in ("NS", "EW", "pedestrian", "clearance")) == CYCLE
    assert result["NS"] >= MIN_GREEN and result["EW"] >= MIN_GREEN
    assert result["pedestrian"] >= MIN_PEDESTRIAN
    return result


def solve_all_csp():
    return {j: solve_full_csp(d) for j, d in DEMAND.items()}


def load_zone_metadata():
    path = Path(__file__).with_name("zone_metadata.json")
    return json.loads(path.read_text(encoding="utf-8"))


def protected_nodes(metadata=None):
    metadata = metadata if metadata is not None else load_zone_metadata()
    return set(metadata.get("school_nodes", [])) | set(
        metadata.get("residential_nodes", [])
    )


def shortest_route(road_graph, start, goal, forbidden=()):
    """Minimum-cost route while avoiding configured protected nodes."""
    forbidden = set(forbidden)
    queue = [(0.0, start, [start])]
    best = {start: 0.0}

    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost > best.get(node, float("inf")):
            continue
        if node == goal:
            return path, cost

        for nxt, weight in road_graph.get(node, {}).items():
            if nxt in forbidden and nxt != goal:
                continue
            if weight < 0:
                raise ValueError("Road costs must be non-negative")
            new_cost = cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(queue, (new_cost, nxt, path + [nxt]))

    return [], float("inf")


def emergency_priority_request(route, schedules, phase_by_junction=None):
    """Produce safe simulated timing requests; does not operate real hardware."""
    phase_by_junction = phase_by_junction or {}
    requests = []

    for junction in route:
        if junction not in schedules:
            continue

        phase = phase_by_junction.get(junction)
        if phase not in ("NS", "EW"):
            continue

        current = schedules[junction]
        other = "EW" if phase == "NS" else "NS"
        if current[other] - EMERGENCY_BONUS < MIN_GREEN:
            continue

        adjusted = dict(current)
        adjusted[phase] += EMERGENCY_BONUS
        adjusted[other] -= EMERGENCY_BONUS

        assert adjusted["NS"] + adjusted["EW"] + adjusted["pedestrian"] + adjusted["clearance"] == CYCLE
        assert adjusted["pedestrian"] >= MIN_PEDESTRIAN
        requests.append({
            "junction": junction,
            "priority_phase": phase,
            "schedule": adjusted,
            "simulation_only": True,
        })

    return requests


def average_trip_cost(trips, schedules, node_to_junction):
    """Illustrative travel cost plus expected red-light wait at mapped nodes."""
    values = []

    for start, goal in trips:
        path, road_cost = shortest_route(graph, start, goal)
        if not path:
            raise ValueError(f"No route for {start} -> {goal}")

        total = road_cost
        for node in path[1:-1]:
            junction = node_to_junction.get(node)
            if junction not in schedules:
                continue

            signal = schedules[junction]
            for phase in ("NS", "EW"):
                green = signal[phase]
                # Uniform arrival approximation for this phase.
                total += (signal["cycle"] - green) ** 2 / (
                    2 * signal["cycle"]
                ) / 2

        values.append(total)

    return sum(values) / len(values)


def main():
    schedules = solve_all_csp()
    print("1. CSP WITH EXPLICIT PEDESTRIAN PHASE")
    for junction, schedule in schedules.items():
        print(junction, schedule)
    print("Fixed cycle, minimum green, pedestrian minimum and exclusive NS/EW phases validated.")

    metadata = load_zone_metadata()
    zones = protected_nodes(metadata)
    print("\n2. PROTECTED-ZONE ROUTING")
    print("Configured school/residential nodes:", sorted(zones))
    start, goal = "Boys Hostel", "Main Gate"
    path, cost = shortest_route(graph, start, goal, zones)
    print("Route:", " -> ".join(path) if path else "No permitted route")
    print("Cost:", round(cost, 2))
    if not zones:
        print("WARNING: zone metadata is empty; real school/residential avoidance is not configured.")

    print("\n3. EMERGENCY SIGNAL PRIORITY")
    print(emergency_priority_request(
        ["J1", "J2"], schedules, {"J1": "NS", "J2": "EW"}
    ))
    print("Simulated requests only; no physical signals are controlled.")

    # Explicit synthetic node-to-junction mapping for evaluation.
    node_map = {
        "Girls Hostel": "J1",
        "Food Court": "J2",
        "Sports Complex": "J3",
        "Parking": "J4",
    }
    baseline = {
        j: {
            "NS": 35, "EW": 35, "pedestrian": 10,
            "clearance": CLEARANCE, "cycle": CYCLE
        } for j in DEMAND
    }
    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
        ("Sports Complex", "Main Gate"),
        ("Parking", "Boys Hostel"),
        ("Gym", "Girls Hostel"),
    ]
    before = average_trip_cost(trips, baseline, node_map)
    after = average_trip_cost(trips, schedules, node_map)
    print("\n4. SYNTHETIC BEFORE/AFTER COMPARISON")
    print(f"Baseline mean cost: {before:.2f}")
    print(f"CSP mean cost: {after:.2f}")
    print(f"Change (positive means improvement): {(before-after)/before*100:.2f}%")
    print("This is a synthetic estimate, not validated real-world travel time.")

    print("\n5. RESPONSIBLE AI")
    print("- Obtain consent and minimize GPS collection and retention.")
    print("- Audit routing outcomes for school and residential impacts.")
    print("- Verify zone metadata before enabling restrictions.")
    print("- Validate timings and emergency pre-emption with traffic engineers.")


if __name__ == "__main__":
    main()
