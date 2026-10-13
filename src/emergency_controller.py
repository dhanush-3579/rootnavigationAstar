
"""Simulation-only emergency signal priority controller."""
from copy import deepcopy
from traffic_csp import CYCLE, CLEARANCE, MIN_GREEN
from final_remaining import MIN_PEDESTRIAN


def request_green_corridor(route, schedules, phase_by_junction):
    """Create safe simulated priority plans; never controls physical hardware."""
    plans = {}
    for junction in route:
        if junction not in schedules:
            continue
        phase = phase_by_junction.get(junction)
        if phase not in ("NS", "EW"):
            raise ValueError(f"Missing or invalid phase for {junction}")

        current = schedules[junction]
        other = "EW" if phase == "NS" else "NS"
        revised = deepcopy(current)

        # Transfer green time only if the opposing phase remains safe.
        transfer = min(5, revised[other] - MIN_GREEN)
        if transfer <= 0:
            plans[junction] = {
                "schedule": revised,
                "simulation_only": True,
            }
            continue



        revised[phase] += transfer
        revised[other] -= transfer

        assert revised["NS"] >= MIN_GREEN
        assert revised["EW"] >= MIN_GREEN
        assert revised["pedestrian"] >= MIN_PEDESTRIAN
        assert revised["clearance"] == CLEARANCE
        assert revised["NS"] + revised["EW"] + revised["pedestrian"] + revised["clearance"] == CYCLE

        plans[junction] = {
            "schedule": revised,
            "priority_phase": phase,
            "simulation_only": True,
        }
    return plans
