
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import math
import pytest

from graph import graph, coordinates
from final_completion import (
    astar_safe, dijkstra, expected_cost_route, schedules_for,
    emergency_priority_plan, simulate_average_trip_cost,
)


def test_astar_matches_dijkstra_on_original_graph():
    _, a_cost, _ = astar_safe(
        graph, coordinates, "Boys Hostel", "Main Gate"
    )
    _, d_cost = dijkstra(graph, "Boys Hostel", "Main Gate")
    assert a_cost == pytest.approx(d_cost)


def test_astar_matches_dijkstra_after_accident():
    from incident_rules import IncidentManager
    manager = IncidentManager(graph)
    manager.accident("Boys Hostel", "Food Court")
    updated = manager.get_updated_graph()

    _, a_cost, _ = astar_safe(
        updated, coordinates, "Boys Hostel", "Main Gate"
    )
    _, d_cost = dijkstra(updated, "Boys Hostel", "Main Gate")
    assert a_cost == pytest.approx(d_cost)


def test_expected_cost_route_avoids_restricted_node():
    path, cost = expected_cost_route(
        graph, "Boys Hostel", "Main Gate",
        {("Boys Hostel", "Food Court"): [(0.5, 4.5), (0.5, 20.0)]},
        forbidden_nodes={"Food Court"},
    )
    assert path
    assert "Food Court" not in path
    assert math.isfinite(cost)


def test_csp_schedules_and_emergency_priority_request():
    schedules = schedules_for(True)
    assert len(schedules) == 4
    plan = emergency_priority_plan(
        ["Boys Hostel", "Girls Hostel", "Food Court"], schedules
    )
    assert plan["simulation_only"]
    assert plan["priority_requests"]


def test_csp_simulation_returns_finite_comparison():
    trips = [
        ("Boys Hostel", "Main Gate"),
        ("Girls Hostel", "Parking"),
        ("Food Court", "Gym"),
    ]
    baseline = simulate_average_trip_cost(trips, schedules_for(False))
    optimized = simulate_average_trip_cost(trips, schedules_for(True))
    assert math.isfinite(baseline)
    assert math.isfinite(optimized)
    assert baseline > 0 and optimized > 0
