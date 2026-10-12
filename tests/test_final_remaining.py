
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graph import graph
from final_remaining import (
    solve_full_csp, solve_all_csp, shortest_route,
    protected_nodes, emergency_priority_request,
)
from traffic_csp import DEMAND, CYCLE, CLEARANCE, MIN_GREEN


def test_explicit_pedestrian_phase_and_cycle():
    for demand in DEMAND.values():
        s = solve_full_csp(demand)
        assert s["NS"] >= MIN_GREEN
        assert s["EW"] >= MIN_GREEN
        assert s["pedestrian"] >= 10
        assert s["NS"] + s["EW"] + s["pedestrian"] + CLEARANCE == CYCLE


def test_all_four_junctions_have_pedestrian_timing():
    schedules = solve_all_csp()
    assert len(schedules) == 4
    assert all(s["pedestrian"] >= 10 for s in schedules.values())


def test_configured_zone_is_avoided():
    path, cost = shortest_route(
        graph, "Boys Hostel", "Main Gate", forbidden={"Food Court"}
    )
    assert path
    assert "Food Court" not in path
    assert cost > 0


def test_zone_metadata_is_read():
    assert protected_nodes({
        "school_nodes": ["Food Court"],
        "residential_nodes": ["Parking"],
    }) == {"Food Court", "Parking"}


def test_emergency_request_preserves_cycle_and_pedestrian_time():
    schedules = solve_all_csp()
    requests = emergency_priority_request(
        ["J1"], schedules, {"J1": "NS"}
    )
    assert requests
    s = requests[0]["schedule"]
    assert s["NS"] + s["EW"] + s["pedestrian"] + s["clearance"] == CYCLE
    assert s["pedestrian"] >= 10
