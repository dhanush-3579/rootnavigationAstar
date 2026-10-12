import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from graph import graph
from incident_rules import IncidentManager
from dynamic_routing import astar_route
from congestion import expected_travel_time


def test_accident_causes_rerouting():
    original_path, original_cost = astar_route(
        graph, "Boys Hostel", "Main Gate"
    )
    assert original_path

    # Block the first edge of the original shortest route.
    source, destination = original_path[0], original_path[1]
    manager = IncidentManager(graph)
    manager.accident(source, destination)

    updated = manager.get_updated_graph()
    new_path, new_cost = astar_route(
        updated, "Boys Hostel", "Main Gate"
    )

    assert new_path
    assert (source, destination) not in list(zip(new_path, new_path[1:]))
    assert new_cost >= original_cost


def test_rain_night_increases_cost():
    manager = IncidentManager(graph)
    manager.set_weather(rain=True, night=True)
    updated = manager.get_updated_graph()

    assert updated["Boys Hostel"]["Girls Hostel"] == pytest.approx(
        graph["Boys Hostel"]["Girls Hostel"] / 0.7
    )


def test_emergency_corridor_is_recorded():
    manager = IncidentManager(graph)
    route = ["Boys Hostel", "Food Court", "Parking", "Main Gate"]
    manager.emergency_vehicle(route)
    assert manager.emergency_corridor == route


def test_route_cost_matches_path_edges():
    manager = IncidentManager(graph)
    manager.accident("Boys Hostel", "Girls Hostel")
    updated = manager.get_updated_graph()
    path, cost = astar_route(updated, "Boys Hostel", "Main Gate")

    assert path[0] == "Boys Hostel"
    assert path[-1] == "Main Gate"
    assert cost == pytest.approx(
        sum(updated[a][b] for a, b in zip(path, path[1:]))
    )


def test_expected_travel_time():
    assert expected_travel_time(
        [(0.6, 7.0), (0.4, 12.0)]
    ) == pytest.approx(9.0)
