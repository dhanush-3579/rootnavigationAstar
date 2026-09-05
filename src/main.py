# main.py

from astar import a_star, bfs


def main():
    print("=== Campus Route Navigation ===")
    print("Available locations:")
    print("Boys Hostel")
    print("Girls Hostel")
    print("Food Court")
    print("Sports Complex")
    print("Gym")
    print("Parking")
    print("Main Gate")

    start = input("\nEnter start location: ")
    goal = input("Enter destination: ")

    if start == goal:
        print("Start and destination are the same.")
        return

    try:
        astar_path, astar_cost, astar_nodes = a_star(start, goal)

        bfs_path, bfs_hops, bfs_nodes = bfs(start, goal)

        print("\n--- A* Result ---")

        if astar_path is None:
            print("No route found.")
        else:
            print("Path:", " -> ".join(astar_path))
            print("Total cost:", round(astar_cost, 2))
            print("Nodes expanded:", astar_nodes)

        print("\n--- BFS Comparison ---")

        if bfs_path is None:
            print("No route found.")
        else:
            print("Path:", " -> ".join(bfs_path))
            print("Number of hops:", bfs_hops)
            print("Nodes expanded:", bfs_nodes)

    except KeyError:
        print("Invalid location. Please enter a location from the list.")


if __name__ == "__main__":
    main()