import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graph import graph
from evaluate_traffic import JUNCTIONS, shortest_path, validate_schedules


def test_signal_schedules_are_valid():
    validate_schedules()

    assert len(JUNCTIONS) == 4

    for schedule in JUNCTIONS.values():
        assert schedule["NS"] >= 15
        assert schedule["EW"] >= 15
        assert (
            schedule["NS"]
            + schedule["EW"]
            + schedule["clearance"]
            == schedule["cycle"]
        )


def test_baseline_route_exists():
    path, cost = shortest_path(
        graph,
        "Boys Hostel",
        "Main Gate",
        lambda u, v, weight: weight,
    )

    assert path is not None
    assert path[0] == "Boys Hostel"
    assert path[-1] == "Main Gate"
    assert cost < float("inf")