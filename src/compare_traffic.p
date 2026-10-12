"""Compare baseline and CSP-optimized signal waiting on simulated trips."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import graph
from dynamic_routing import astar_route
from traffic_csp import DEMAND, solve_junction, validate_schedules


TRIPS = [
    ("Boys Hostel", "Main Gate"),
    ("Girls Hostel", "Parking"),
    ("Food Court", "Gym"),
    ("Sports Complex", "Main Gate"),
    ("Parking", "Boys Hostel"),
    ("Gym", "Girls Hostel"),
]


def make_schedules(optimized):
    if optimized:
        schedules = {
            junction: solve_junction(demand)
            for junction, demand in DEMAND.items()
        }
    else:
        # Explicit illustrative baseline: equal green phases.
        schedules = {
            junction: {
                "NS": 40, "EW": 40,
                "clearance": 10, "cycle": 90,
            }
            for junction in DEMAND
        }

    validate_schedules(schedules)
    return schedules


def mean_signal_wait(schedules):
    # Uniform-arrival approximation for each phase:
    # average red wait = (cycle - green) ** 2 / (2 * cycle)
    total = 0.0
    count = 0

    for signal in schedules.values():
        cycle = signal["cycle"]
        for phase in ("NS", "EW"):
            green = signal[phase]
            total += (cycle - green) ** 2 / (2 * cycle)
            count += 1

    return total / count if count else 0.0


def evaluate(schedules):
    signal_wait = mean_signal_wait(schedules)
    trip_costs = []

    for start, goal in TRIPS:
        path, road_cost = astar_route(graph, start, goal)
        if not path:
            raise RuntimeError(f"No route: {start} -> {goal}")

        # Approximate exposure to junction delays:
        # one signal wait per intermediate route node.
        junction_count = max(0, len(path) - 2)
        trip_costs.append(road_cost + junction_count * signal_wait)

    return sum(trip_costs) / len(trip_costs)


def main():
    baseline_schedules = make_schedules(optimized=False)
    optimized_schedules = make_schedules(optimized=True)

    before = evaluate(baseline_schedules)
    after = evaluate(optimized_schedules)
    improvement = (before - after) / before * 100 if before else 0.0

    print("SIMULATED TRAFFIC SIGNAL COMPARISON")
    print(f"Trips evaluated: {len(TRIPS)}")
    print(f"Baseline average estimated cost: {before:.2f}")
    print(f"CSP average estimated cost:      {after:.2f}")
    print(f"Estimated improvement:           {improvement:.2f}%")
    print("\nCSP schedules:")
    for junction, signal in optimized_schedules.items():
        print(
            f"{junction}: NS={signal['NS']}s, EW={signal['EW']}s, "
            f"clearance={signal['clearance']}s, cycle={signal['cycle']}s"
        )

    print(
        "\nLimitations: illustrative equal-green baseline; simplified "
        "junction-delay model; no road-to-junction mapping or queue "
        "simulation. Results are estimates, not real-world measurements."
    )


if __name__ == "__main__":
    main()
