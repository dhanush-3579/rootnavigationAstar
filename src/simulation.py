"""Simulated before-versus-after traffic optimisation experiment."""

import random
import statistics

from congestion import expected_travel_time


def generate_trips(number_of_trips=100, seed=42):
    """Generate reproducible simulated trips in minutes."""
    rng = random.Random(seed)
    trips = []

    for _ in range(number_of_trips):
        baseline = rng.uniform(8.0, 18.0)

        # Illustrative effects of coordinated signals and routing.
        signal_saving = rng.uniform(0.5, 2.0)
        routing_saving = rng.uniform(0.0, 1.5)
        incident_delay = rng.uniform(0.0, 1.0)

        optimised = max(
            1.0,
            baseline - signal_saving - routing_saving + incident_delay,
        )

        trips.append((baseline, optimised))

    return trips


def main():
    trips = generate_trips()

    baseline_times = [before for before, _ in trips]
    optimised_times = [after for _, after in trips]

    before = statistics.mean(baseline_times)
    after = statistics.mean(optimised_times)
    improvement = (before - after) / before * 100.0

    print("SMART TRAFFIC MANAGEMENT SIMULATION")
    print("Trips simulated:", len(trips))
    print()
    print(f"Average travel time before: {before:.2f} minutes")
    print(f"Average travel time after:  {after:.2f} minutes")
    print(f"Average time saved:         {before - after:.2f} minutes")
    print(f"Travel-time improvement:    {improvement:.2f}%")

    print("\nExample expected travel time:")
    scenarios = [(0.6, 7.0), (0.4, 12.0)]
    print(f"E[T] = {expected_travel_time(scenarios):.2f} minutes")

    print(
        "\nNOTE: These are synthetic demonstration data. "
        "Replace this simplified model with trips evaluated on your "
        "actual road graph and CSP signal plan for final evaluation."
    )


if __name__ == "__main__":
    main()