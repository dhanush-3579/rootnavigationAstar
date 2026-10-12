"""Map CSP junction IDs to actual campus graph locations."""

JUNCTION_TO_NODE = {
    "J1": None,  # Replace with the actual graph node
    "J2": None,  # Replace with the actual graph node
    "J3": None,  # Replace with the actual graph node
    "J4": None,  # Replace with the actual graph node
}


def validate_mapping(graph):
    for junction, node in JUNCTION_TO_NODE.items():
        if node is None:
            raise ValueError(
                f"Assign an actual graph location to {junction}"
            )
        if node not in graph:
            raise ValueError(
                f"{junction} maps to unknown graph node: {node}"
            )