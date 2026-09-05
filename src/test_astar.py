import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from astar import a_star, bfs


def test_astar_finds_path():
    path, cost, nodes = a_star("Main Gate", "Food Court")

    assert path is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Food Court"
    assert cost > 0
    assert nodes > 0


def test_bfs_finds_path():
    path, hops, nodes = bfs("Main Gate", "Food Court")

    assert path is not None
    assert path[0] == "Main Gate"
    assert path[-1] == "Food Court"
    assert hops > 0
    assert nodes > 0