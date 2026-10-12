
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from graph import graph
from project_extension import (
    dijkstra, route_with_expected_cost, signal_plan,
    emergency_signal_plan
)


def test_astar_route_cost_can_be_checked_against_dijkstra():
    from dynamic_routing import astar_route
    path_a, cost_a = astar_route(graph, "Boys Hostel", "Main Gate")
    path_d, cost_d = dijkstra(graph, "Boys Hostel", "Main Gate")
    assert path_a and path_d
    assert cost_a == pytest.approx(cost_d)


def test_expected_cost_route_and_zone_avoidance():
    path, cost = route_with_expected_cost(
        graph, "Boys Hostel", "Main Gate",
        edge_scenarios={
            ("Boys Hostel", "Food Court"): [(0.5, 4.5), (0.5, 20.0)]
        },
        forbidden={"Food Court"}
    )
    assert path
    assert "Food Court" not in path
    assert cost >= 0


def test_csp_and_emergency_priority_plan():
    schedules = signal_plan()
    assert len(schedules) == 4
    result = emergency_signal_plan(
        ["Boys Hostel", "Food Court", "Parking"], schedules
    )
    assert result["priority"] is True
    assert result["route"][0] == "Boys Hostel"
