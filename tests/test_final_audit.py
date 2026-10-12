
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from traffic_csp import DEMAND, CYCLE, CLEARANCE, MIN_GREEN
from final_audit import optimize_junction, optimize_all, validate


def test_optimizer_respects_all_signal_constraints():
    schedules = optimize_all()
    assert len(schedules) == 4
    validate(schedules)
    for schedule in schedules.values():
        assert schedule["pedestrian"] >= 10
        assert schedule["NS"] >= MIN_GREEN
        assert schedule["EW"] >= MIN_GREEN
        assert schedule["NS"] + schedule["EW"] + schedule["pedestrian"] + CLEARANCE == CYCLE


def test_optimizer_is_no_worse_than_equal_green_for_signal_objective():
    for junction, demand in DEMAND.items():
        result = optimize_junction(demand)
        def objective(ns, ew):
            return (
                demand["NS"] * (CYCLE - ns) ** 2
                + demand["EW"] * (CYCLE - ew) ** 2
            )
        assert objective(result["NS"], result["EW"]) <= objective(35, 35)
