import heapq
from graph import graph
from incident_rules import IncidentManager


def astar_dynamic(road_graph, start, goal):
    """Find an optimal route using non-negative edge costs."""
    if start not in road_graph or goal not in road_graph:
        raise ValueError("Unknown start or destination.")

    queue = [(0.0, start)]
    costs = {start: 0.0}
    parents = {start: None}

    while queue:
        cost, current = heapq.heappop(queue)

        if cost > costs[current]:
            continue

        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parents[node]
            return list(reversed(path)), cost

        for neighbour, edge_cost in road_graph[current].items():
            if edge_cost < 0:
                raise ValueError("Edge costs must be non-negative.")

            new_cost = cost + edge_cost
            if new_cost < costs.get(neighbour, float("inf")):
                costs[neighbour] = new_cost
                parents[neighbour] = current
                heapq.heappush(queue, (new_cost, neighbour))

    return None, float("inf")


def main():
    manager = IncidentManager(graph)
    locations = list(graph)
    lookup = {name.casefold(): name for name in locations}

    print("Available locations:")
    for name in locations:
        print("-", name)

    start_text = input("Enter start location: ").strip().casefold()
    goal_text = input("Enter destination: ").strip().casefold()

    if start_text not in lookup or goal_text not in lookup:
        print("Invalid location.")
        return

    start, goal = lookup[start_text], lookup[goal_text]

    baseline_path, baseline_cost = astar_dynamic(graph, start, goal)
    print("\nBASELINE ROUTE")
    print("Path:", " -> ".join(baseline_path or []))
    print("Cost:", baseline_cost)

    print("\n1. Rain and night")
    print("2. Accident on a road")
    print("3. No incident")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        manager.set_weather(rain=True, night=True)

    elif choice == "2":
        source_text = input("Road source: ").strip().casefold()
        dest_text = input("Road destination: ").strip().casefold()

        if source_text not in lookup or dest_text not in lookup:
            print("Invalid road locations.")
            return

        source, destination = lookup[source_text], lookup[dest_text]

        if destination not in graph.get(source, {}):
            print("That directed road does not exist.")
            return

        manager.accident(source, destination)

    elif choice != "3":
        print("Invalid choice.")
        return

    updated_graph = manager.get_updated_graph()
    new_path, new_cost = astar_dynamic(updated_graph, start, goal)

    print("\nUPDATED ROUTE")
    if new_path is None:
        print("No available route.")
    else:
        print("Path:", " -> ".join(new_path))
        print("Cost:", round(new_cost, 2))


if __name__ == "__main__":
    main()
