
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graph import graph
from final_remaining import shortest_route, protected_nodes
from final_audit import optimize_all
from emergency_controller import request_green_corridor
from traffic_csp import CYCLE, CLEARANCE, MIN_GREEN


def test_configured_zones_are_avoided():
    zones = protected_nodes()
    assert zones
    path, cost = shortest_route(
        graph, "Boys Hostel", "Main Gate", forbidden=zones
    )
    assert path
    assert not (set(path) & (zones - {"Main Gate"}))


def test_zone_metadata_names_exist_in_graph():
    data = json.loads(Path("src/zone_metadata.json").read_text())
    for node in data["school_nodes"] + data["residential_nodes"]:
        assert node in graph


def test_emergency_plan_preserves_cycle_and_safety():
    schedules = optimize_all()
    plans = request_green_corridor(
        ["J1", "J2"], schedules, {"J1": "NS", "J2": "EW"}
    )
    assert len(plans) == 2
    for plan in plans.values():
        s = plan["schedule"]
        assert plan["simulation_only"] is True
        assert s["NS"] >= MIN_GREEN and s["EW"] >= MIN_GREEN
        assert s["NS"] + s["EW"] + s["pedestrian"] + s["clearance"] == CYCLE
        assert s["pedestrian"] >= 10
