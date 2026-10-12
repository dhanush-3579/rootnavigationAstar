"""Probabilistic congestion model for smart traffic routing."""

def expected_travel_time(scenarios):
    """
    Calculate expected travel time.

    scenarios is a list of (probability, travel_time) pairs.
    Probabilities must sum to 1.
    """
    if not scenarios:
        raise ValueError("At least one scenario is required.")

    total_probability = sum(probability for probability, _ in scenarios)

    if any(probability < 0 for probability, _ in scenarios):
        raise ValueError("Probabilities cannot be negative.")

    if any(travel_time < 0 for _, travel_time in scenarios):
        raise ValueError("Travel times cannot be negative.")

    if abs(total_probability - 1.0) > 1e-9:
        raise ValueError("Scenario probabilities must sum to 1.")

    return sum(
        probability * travel_time
        for probability, travel_time in scenarios
    )


def sample_road_conditions():
    """Return illustrative travel-time scenarios in minutes."""
    return {
        "Road A": [
            (0.6, 7.0),
            (0.4, 12.0),
        ],
        "Road B": [
            (0.8, 8.0),
            (0.2, 10.0),
        ],
        "Road C": [
            (0.5, 4.0),
            (0.5, 6.0),
        ],
    }


def main():
    print("PROBABILISTIC CONGESTION MODEL")
    print("Expected travel time = sum(probability * travel time)\n")

    roads = sample_road_conditions()

    for road, scenarios in roads.items():
        expected = expected_travel_time(scenarios)
        print(f"{road}: expected travel time = {expected:.2f} minutes")


if __name__ == "__main__":
    main()