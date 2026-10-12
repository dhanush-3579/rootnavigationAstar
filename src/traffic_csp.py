
"""CSP traffic signal optimizer using backtracking and propagation."""

CYCLE = 90
CLEARANCE = 10
MIN_GREEN = 15

DEMAND = {
    "J1": {"NS": 80, "EW": 40},
    "J2": {"NS": 30, "EW": 75},
    "J3": {"NS": 65, "EW": 45},
    "J4": {"NS": 25, "EW": 90},
}


def solve_junction(demand):
    """Find integer green durations satisfying the CSP constraints."""
    green_total = CYCLE - CLEARANCE

    # Domains: both phases must be >= MIN_GREEN and sum to green_total.
    domains = {
        "NS": list(range(MIN_GREEN, green_total - MIN_GREEN + 1)),
        "EW": list(range(MIN_GREEN, green_total - MIN_GREEN + 1)),
    }

    assignment = {}

    def propagate(variable, value):
        """Forward-check the remaining phase domain."""
        remaining = green_total - value
        other = "EW" if variable == "NS" else "NS"

        if remaining not in domains[other]:
            return False

        domains[other] = [remaining]
        return True

    def backtrack():
        if len(assignment) == 2:
            return (
                assignment["NS"] + assignment["EW"] == green_total
            )

        variable = next(v for v in ("NS", "EW") if v not in assignment)

        # Prefer timings proportional to traffic demand.
        values = sorted(
            domains[variable],
            key=lambda green: abs(
                green / green_total
                - demand[variable] / (demand["NS"] + demand["EW"])
            ),
        )

        original_other = domains[
            "EW" if variable == "NS" else "NS"
        ][:]

        for value in values:
            if value < MIN_GREEN:
                continue

            assignment[variable] = value

            if propagate(variable, value) and backtrack():
                return True

            del assignment[variable]
            domains["EW" if variable == "NS" else "NS"] = (
                original_other[:]
            )

        return False

    if not backtrack():
        raise RuntimeError("No feasible signal schedule found")

    return {
        "NS": assignment["NS"],
        "EW": assignment["EW"],
        "clearance": CLEARANCE,
        "cycle": CYCLE,
    }


def validate_schedules(schedules):
    for junction, signal in schedules.items():
        assert signal["NS"] >= MIN_GREEN, f"{junction}: NS too short"
        assert signal["EW"] >= MIN_GREEN, f"{junction}: EW too short"
        assert (
            signal["NS"] + signal["EW"] + signal["clearance"]
            == signal["cycle"]
        ), f"{junction}: cycle mismatch"


def main():
    schedules = {
        junction: solve_junction(demand)
        for junction, demand in DEMAND.items()
    }

    validate_schedules(schedules)

    print("SMART TRAFFIC MANAGEMENT - CSP OPTIMIZER")
    print("Method: Backtracking + forward checking")
    print(f"Cycle: {CYCLE}s | Clearance: {CLEARANCE}s")
    print(f"Minimum green: {MIN_GREEN}s")

    for junction, signal in schedules.items():
        print(
            f"{junction}: NS={signal['NS']}s, "
            f"EW={signal['EW']}s, "
            f"clearance={signal['clearance']}s, "
            f"cycle={signal['cycle']}s"
        )

    print("\nAll optimized junction schedules passed validation.")


if __name__ == "__main__":
    main()