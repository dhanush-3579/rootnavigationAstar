from astar import a_star, bfs
from graph import graph


def find_location(user_input):
    """Match a location regardless of capitalization or extra spaces."""
    cleaned = user_input.strip().casefold()

    for location in graph:
        if location.strip().casefold() == cleaned:
            return location

    return None


def main():
    locations = list(graph.keys())

    print("\nAvailable locations:")
    for location in locations:
        print(f"- {location}")

    start_input = input("\nEnter start location: ")
    goal_input = input("Enter destination: ")

    start = find_location(start_input)
    goal = find_location(goal_input)

    if start is None or goal is None:
        print("Invalid location. Please enter a location from the list.")
        return

    print("\n========== A* ROUTE ==========")
    path, cost, nodes = a_star(start, goal)

    if path is None:
        print("A*: No route found.")
    else:
        print("A* Path:", " -> ".join(path))
        print(f"Total cost: {cost:.2f}")
        print(f"Nodes expanded: {nodes}")

    print("\n========== BFS ROUTE ==========")
    path, hops, nodes = bfs(start, goal)

    if path is None:
        print("BFS: No route found.")
    else:
        print("BFS Path:", " -> ".join(path))
        print(f"Number of hops: {hops}")
        print(f"Nodes expanded: {nodes}")


if __name__ == "__main__":
    main()