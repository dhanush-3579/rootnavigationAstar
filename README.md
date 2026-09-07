# Root Navigation using A* Algorithm

## 1. Project Overview

Root Navigation is an Artificial Intelligence based campus navigation project that finds the shortest and most efficient route between two locations using the **A* (A-Star) search algorithm**.

The project represents a campus or real-world location as a **weighted graph**, where:

- Each location is represented as a **node**.
- Each road/path between two locations is represented as an **edge**.
- The distance between locations is represented as the **edge weight**.
- A* uses both the actual distance travelled and an estimated distance to the destination to efficiently find the best route.

For example, a user can provide a starting location such as:

`Main Gate`

and a destination such as:

`Food Court`

The system calculates a suitable route between these two locations and returns the path, total cost/distance, and other search information.

The main objective of this project is to demonstrate how Artificial Intelligence search algorithms can be applied to real-world navigation problems.

---

## 2. Problem Statement

Finding an efficient route between two locations is a common problem in navigation systems.

Traditional search algorithms can explore a large number of unnecessary locations before reaching the destination. For example, Breadth-First Search (BFS) is useful for unweighted graphs, but it does not consider the actual distance between locations.

Similarly, Dijkstra's algorithm can find the shortest path in a weighted graph, but it does not use information about the direction of the destination. Because of this, it may explore many unnecessary nodes.

The A* algorithm improves this process by combining:

1. The actual cost from the starting location to the current location.
2. A heuristic estimate of the remaining cost to the destination.

The evaluation function used by A* is:

    f(n) = g(n) + h(n)

where:

- `g(n)` = actual cost from the start node to node `n`
- `h(n)` = estimated cost from node `n` to the goal
- `f(n)` = estimated total cost of the route through node `n`

Therefore, A* can find an optimal path while usually exploring fewer nodes than uninformed search methods.

---

## 3. Objectives

The main objectives of this project are:

- To implement the A* search algorithm.
- To represent a campus navigation system as a weighted graph.
- To find a route between two campus locations.
- To use a heuristic function to guide the search.
- To calculate the total path cost.
- To compare A* with other search algorithms conceptually.
- To demonstrate the use of Artificial Intelligence in navigation.
- To write test cases to verify the correctness of the implementation.
- To maintain proper project documentation.

---

## 4. Why A* Algorithm?

A* was selected because it combines the advantages of cost-based search and heuristic-based search.

### Breadth-First Search (BFS)

BFS is suitable for unweighted graphs. It explores nodes level by level.

However, when paths have different distances, BFS does not guarantee the shortest distance-based route.

### Depth-First Search (DFS)

DFS explores one path deeply before backtracking.

It is simple to implement, but it does not guarantee the shortest route.

### Dijkstra's Algorithm

Dijkstra's algorithm considers the actual path cost and can find the shortest path in a weighted graph.

However, it does not use a heuristic to estimate the remaining distance to the destination.

### Greedy Best-First Search

Greedy Best-First Search uses a heuristic to move toward the destination.

It can be fast, but it does not always produce the shortest path because it ignores the cost already travelled.

### A* Search

A* combines both approaches:

    f(n) = g(n) + h(n)

Therefore, A* considers both:

- How much distance has already been travelled.
- How far the destination is estimated to be.

This makes A* a suitable algorithm for campus navigation.

---

## 5. System Architecture

The project is organized into multiple components.

### 5.1 Graph Model

The campus is represented as a weighted graph.

For example:

    Main Gate
       |
       | distance
       |
    Library
       |
       |
    Food Court

Each location is stored as a node and each connection contains a distance or cost.

The graph allows the navigation system to understand which locations are connected and how much it costs to travel between them.

---

### 5.2 A* Search

The A* algorithm maintains a priority queue of nodes that need to be explored.

For each node, the algorithm calculates:

    f(n) = g(n) + h(n)

The node with the smallest estimated total cost is selected for exploration.

The algorithm continues until the destination is reached.

During the search, the system stores the previous node of each visited location. This allows the final route to be reconstructed after reaching the destination.

---

### 5.3 Heuristic Function

The heuristic estimates the remaining distance between the current location and the destination.

A good heuristic helps A* reduce unnecessary exploration.

For coordinate-based locations, a common heuristic is Euclidean distance:

    h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)

The heuristic should not overestimate the actual remaining cost when optimality is required.

---

## 6. Project Structure

The project follows a simple modular structure:

    rootnavigationAstar/
    │
    ├── docs/
    │   └── project_report.md
    │
    ├── tests/
    │   └── test_astar.py
    │
    ├── astar.py
    ├── graph.py
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── LICENSE
    └── .gitignore

### File Description

### `astar.py`

Contains the implementation of the A* search algorithm.

It is responsible for:

- Exploring graph nodes.
- Calculating path costs.
- Applying the heuristic.
- Selecting the next node.
- Reconstructing the final path.

### `graph.py`

Contains the graph representation used by the navigation system.

It defines the campus locations and the connections between them.

### `main.py`

Acts as the main entry point of the application.

It can be used to run the navigation system and test routes between different locations.

### `tests/test_astar.py`

Contains test cases for verifying the A* implementation.

The tests check whether the algorithm correctly finds a path and whether the returned path starts from the requested source.

### `docs/project_report.md`

Contains the detailed project report, including the problem description, system architecture, algorithm explanation, testing, and references.

### `requirements.txt`

Contains the Python dependencies required to run the project.

---

## 7. Algorithm Workflow

The A* navigation process can be summarized as follows:

1. Select the starting location.
2. Select the destination.
3. Initialize the priority queue.
4. Calculate the initial heuristic value.
5. Add the starting node to the queue.
6. Select the node with the lowest `f(n)` value.
7. Check whether it is the destination.
8. If the destination is reached, reconstruct the path.
9. Otherwise, examine its neighbouring nodes.
10. Calculate the new path cost for each neighbour.
11. Calculate the heuristic value.
12. Calculate the total estimated cost.
13. Add or update the neighbour in the priority queue.
14. Continue until the destination is reached or no path exists.

### Pseudocode

    A*(start, goal):

        open_set = priority queue
        add start to open_set

        g_score[start] = 0
        f_score[start] = h(start, goal)

        while open_set is not empty:

            current = node with lowest f_score

            if current == goal:
                return reconstructed path

            for each neighbour of current:

                tentative_g = g_score[current] + cost(current, neighbour)

                if tentative_g is better than previous cost:

                    store current as neighbour's parent

                    g_score[neighbour] = tentative_g

                    f_score[neighbour] =
                        g_score[neighbour] + h(neighbour, goal)

                    add neighbour to open_set

        return no path found

---

## 8. Example

Suppose the user wants to travel from:

    Start: Main Gate

to:

    Destination: Food Court

The graph contains multiple possible routes.

A* does not blindly explore every route. Instead, it calculates the cost of reaching each node and estimates how close the node is to the destination.

For each node:

    f(n) = g(n) + h(n)

The algorithm gives priority to the node with the lowest estimated total cost.

After reaching the destination, the algorithm reconstructs the path using the stored parent information.

The result can be represented as:

    Main Gate
        ↓
    Library
        ↓
    Food Court

The system can also calculate the total travel cost associated with the selected path.

---

## 9. Testing

Testing is an important part of the project because the navigation algorithm must return a valid route.

The project contains automated tests in:

    tests/test_astar.py

One of the tests verifies that a route exists between:

    Main Gate

and:

    Food Court

The test checks that:

- A path is returned.
- The path is not `None`.
- The first node in the path is the starting location.

Example:

    path, hops, nodes = bfs("Main Gate", "Food Court")

    assert path is not None
    assert path[0] == "Main Gate"

The test structure helps ensure that the navigation implementation behaves as expected.

Additional tests can be added for:

- Valid source and destination.
- Same source and destination.
- Unreachable destinations.
- Different paths.
- Correct path cost.
- Heuristic behaviour.

---

## 10. Advantages

The A* based navigation system provides several advantages:

- Finds efficient routes in weighted graphs.
- Uses a heuristic to guide the search.
- Avoids unnecessary exploration in many cases.
- Can be adapted to real campus maps.
- Supports different path costs.
- Demonstrates an important Artificial Intelligence search technique.
- Modular Python implementation makes the project easy to modify.

---

## 11. Limitations

Although A* is powerful, the system has some limitations:

- The quality of the result depends on the graph representation.
- A poor heuristic can make the search less efficient.
- The graph must contain accurate location and distance information.
- Large graphs can require significant memory.
- The current project represents a simplified campus environment rather than a complete real-world navigation service.
- Dynamic conditions such as traffic, blocked roads, or temporary construction are not automatically considered unless they are added to the graph.

---

## 12. Future Enhancements

The project can be extended in several ways.

### Real Campus Map

Actual campus locations and road networks can be integrated into the graph.

### GPS Integration

GPS coordinates can be used to determine the user's current location.

### Graphical Interface

A graphical user interface can display:

- Campus map.
- Current location.
- Destination.
- Calculated route.
- Total distance.

### Dynamic Navigation

The system could support changing road conditions such as:

- Blocked paths.
- Construction areas.
- Temporary closures.
- Changing travel costs.

### Multiple Transportation Modes

Different costs could be assigned for:

- Walking.
- Cycling.
- Vehicles.

### Voice Navigation

Voice instructions could be added to guide the user from one location to another.

---

## 13. Complexity

The performance of A* depends on the graph and heuristic used.

For a graph with many nodes and edges, the algorithm may require significant memory because it stores nodes that are waiting to be explored.

The heuristic plays an important role in performance.

A good heuristic reduces the number of unnecessary nodes explored, while a poor heuristic can make A* behave more like Dijkstra's algorithm.

When the heuristic is admissible, A* can provide an optimal shortest path under the standard conditions of the search problem.

---

## 14. Technologies Used

The project is implemented using:

- **Python**
- **A* Search Algorithm**
- **Graph Data Structure**
- **Priority Queue**
- **Heuristic Function**
- **Pytest / Python Testing**
- **Git**
- **GitHub**
- **Markdown**

---

## 15. How to Run the Project

### Step 1: Clone the Repository

Clone the project repository from GitHub.

    git clone https://github.com/dhanush-3579/rootnavigationAstar.git

### Step 2: Navigate to the Project

    cd rootnavigationAstar

### Step 3: Install Requirements

If required, install the dependencies:

    pip install -r requirements.txt

### Step 4: Run the Application

    python main.py

### Step 5: Run Tests

    pytest

The test command executes the available test cases and helps verify the correctness of the implementation.

---

## 16. GitHub Repository

The complete project source code, tests, documentation, and report are maintained in the GitHub repository:

**Root Navigation A\* Repository**

https://github.com/dhanush-3579/rootnavigationAstar

---

## 17. Conclusion

The Root Navigation project demonstrates how Artificial Intelligence can be applied to a practical navigation problem using the A* search algorithm.

The campus environment is represented as a weighted graph, where locations are nodes and paths are weighted edges. A* combines the actual cost travelled with a heuristic estimate of the remaining distance to efficiently search for a suitable route.

The project also demonstrates important software development practices such as modular programming, automated testing, documentation, and version control using Git and GitHub.

Overall, this project provides a practical implementation of A* and shows why heuristic search algorithms are useful for navigation and path-finding applications.

---

## 18. References

1. Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*.
3. Hart, P. E., Nilsson, N. J., and Raphael, B. (1968), *A Formal Basis for the Heuristic Determination of Minimum Cost Paths*.
4. A* Search Algorithm concepts and graph-search resources.
5. Python documentation for data structures and testing.