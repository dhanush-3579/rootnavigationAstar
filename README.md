Smart Campus Route Navigation Using A* and CSP-Based Traffic Management

A Python-based campus navigation project that implements A* search for weighted shortest-path routing and extends it with Constraint Satisfaction Problem (CSP)-based traffic signal scheduling.

The project explores how graph search, constraint solving, and traffic simulation can work together to support intelligent route planning.

Table of Contents
Project Overview
Objectives
Implemented Features
Technology Stack
Project Structure
Installation
Running the Project
Testing
Algorithms and Design
Example Campus Route
Traffic Signal Scheduling
Current Limitations
Future Improvements
Responsible AI Considerations
License
Project Overview

Campus navigation can be modeled as a weighted graph in which locations are vertices and roads are weighted edges. A search algorithm can determine a route between two locations while minimizing the sum of edge costs.

This project uses A* search with a straight-line-distance heuristic to find routes through a campus graph. Breadth-First Search (BFS) is also implemented for comparison, and a Dijkstra-based verification program checks whether A* returns optimal path costs for the tested start-destination pairs.

The project also includes a CSP-based traffic signal scheduling component for four hypothetical junctions. It validates green-phase durations against configured cycle-length and minimum-phase constraints.

The longer-term goal is to integrate route navigation, traffic signal optimization, incident handling, and simulated travel-time evaluation into a unified Smart Traffic Management System.

Objectives
Find low-cost campus routes using A* search on a weighted graph.
Use an admissible heuristic based on straight-line distance.
demonstrate the A* evaluation function:

f(n) = g(n) + h(n)

Compare A* path costs with Dijkstra's algorithm.
Explore CSP-based traffic signal scheduling for four junctions.
Evaluate theoretical signal waiting times under explicitly stated assumptions.
Establish a foundation for dynamic routing and traffic simulation.
Implemented Features
1. Campus Route Navigation

The campus map is represented as a weighted graph containing locations such as:

Boys Hostel
Girls Hostel
Food Court
Sports Complex
Gym
Parking
Main Gate

Each edge has a numerical weight representing the cost of traveling between two connected locations. The units of these weights have not yet been established as actual time or distance measurements.

2. A* Search

A* evaluates candidate nodes using:

f(n) = g(n) + h(n)

Where:

g(n) is the accumulated path cost from the start node to node n.
h(n) estimates the remaining cost from node n to the destination.
f(n) is the estimated total cost of a route through node n.

The heuristic is based on straight-line distance between campus coordinates. For the heuristic to be admissible, the coordinate scale and edge costs must be compatible, and the heuristic must not overestimate the remaining path cost.

Under these conditions, with nonnegative edge weights and a suitable graph-search implementation, A* can return an optimal route.

3. Breadth-First Search

BFS is implemented as an additional graph-search method. It explores nodes level by level and is useful for comparing traversal behavior.

BFS minimizes the number of edges in an unweighted graph. It does not necessarily minimize the weighted cost of a route when edge weights differ.

4. Dijkstra-Based Optimality Verification

The project includes src/verify_astar.py, which compares A* path costs against an independent Dijkstra implementation across campus location pairs.

The existing verification run reported:

42 start-destination pairs checked.
A* costs matched Dijkstra for all tested pairs.

This supports the correctness of the tested route costs on the current graph. It does not independently establish that the heuristic is admissible for every possible graph or that future dynamic-cost implementations are optimal.

5. CSP Traffic Signal Scheduling

The traffic signal scheduling component models four junctions: J1, J2, J3, and J4.

Configured constraints include:

Cycle length: 90 seconds per junction.
Clearance interval: 10 seconds.
Minimum green duration: 15 seconds per phase.
NS and EW phases must satisfy the cycle-length constraint.
NS and EW greens are treated as mutually exclusive phases at each junction.

The current CSP implementation uses backtracking and forward checking to find feasible green durations. Its demand-proportional objective favors allocating green time according to the relative demand of each approach.

A feasible schedule is not necessarily the schedule that minimizes real-world traffic delay. The current objective has not been demonstrated to be optimal for the complete road network.

6. Traffic Evaluation

The traffic evaluator is implemented in src/evaluate_traffic.py.

It can:

Validate signal schedule constraints.
Generate schedules using the CSP solver.
Calculate theoretical average red-light waiting estimates.
Evaluate shortest-path costs for selected campus trips.
Display route paths and graph costs.
Report limitations associated with the simulation assumptions.

The waiting-time formula assumes uniformly distributed arrivals at a periodic signal:

Average wait = (cycle - green)^2 / (2 × cycle)

This is a theoretical approximation. It does not model vehicle queues, saturation flow, spillback, turning movements, or observed traffic conditions.

Signal waiting estimates and graph costs are currently reported separately because junction-to-road mappings and compatible edge-cost units have not yet been established.

Technology Stack
Language: Python
Testing framework: pytest
Graph algorithms: A*, BFS, Dijkstra
Constraint solving: Backtracking and forward checking
Development environment: Python virtual environment
Version control: Git and GitHub

The routing and traffic logic primarily uses Python's standard library. Install the packages listed in requirements.txt to reproduce the project's configured environment.

Project Structure
rootnavigationAstar/
├── src/
│   ├── graph.py
│   ├── astar.py
│   ├── verify_astar.py
│   ├── traffic_csp.py
│   └── evaluate_traffic.py
├── tests/
│   ├── test_astar.py
│   └── test_traffic_evaluation.py
├── docs/
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore


The tree above describes the intended layout of the project. If the actual filenames differ in your local checkout, use the filenames present in your repository.

Installation
Prerequisites
Python 3.10 or later is recommended.
Git.
PowerShell on Windows, or an equivalent terminal.
1. Clone the repository
git clone https://github.com/dhanush-3579/rootnavigationAstar.git
cd rootnavigationAstar

2. Create a virtual environment

On Windows PowerShell:

python -m venv .venv


Activate it:

.\.venv\Scripts\Activate.ps1


If PowerShell blocks activation, consult your Python environment configuration or activate the environment using the appropriate command for your terminal.

3. Install dependencies
python -m pip install -r requirements.txt

Running the Project

Run the following commands from the repository root.

Run the A* verification
python .\src\verify_astar.py


This compares A* path costs against Dijkstra's shortest-path costs for the tested campus location pairs.

Run the traffic CSP scheduler
python .\src\traffic_csp.py


This generates and validates green-phase schedules for the configured junctions.

Run the traffic evaluator
python .\src\evaluate_traffic.py


This evaluates the configured campus trips and displays theoretical signal-wait estimates.

The scripts depend on the project's Python module layout. If a script cannot resolve an import when executed directly, check that the repository root and src directory are configured consistently with the imports used in the code.

Testing

Run the complete test suite from the repository root:

python -m pytest -v


The latest reported successful test run contained four tests:

Test	Result
test_astar_finds_path	PASSED
test_bfs_finds_path	PASSED
test_signal_schedules_are_valid	PASSED
test_baseline_route_exists	PASSED

The reported result was 4 passed.

These tests cover basic routing, signal-schedule validation, and baseline route existence. They do not yet verify the complete dynamic traffic-management system or demonstrate reduced average travel time.

Algorithms and Design
Weighted Graph

Let the campus road network be represented by a graph:

G = (V, E)

Where:

V is the set of campus locations.
E is the set of road connections.
Each edge has a nonnegative numerical cost.

A path's total cost is the sum of the edge costs along that path.

A* Evaluation

A* ranks search nodes using:

f(n) = g(n) + h(n)

The algorithm balances the cost already incurred with an estimate of the cost remaining.

For optimality, the heuristic must be admissible, and the implementation must correctly handle node expansion and path-cost updates. For this project, straight-line distance is the intended heuristic; its compatibility with the graph's cost units must be maintained.

Dijkstra Verification

Dijkstra's algorithm computes shortest paths for graphs with nonnegative edge weights without relying on a heuristic.

Comparing A* results with Dijkstra provides an independent check of the resulting path costs for the tested graph and start-destination pairs.

CSP Signal Scheduling

For each junction, define:

G_NS: north-south green duration.
G_EW: east-west green duration.
C: cycle duration.
L: clearance duration.
G_min: minimum green duration.

The scheduling constraints are:

G_NS + G_EW + L = C

G_NS >= G_min

G_EW >= G_min

With the current settings:

G_NS + G_EW = 80 seconds

Both phases must receive at least 15 seconds of green time.

The solver searches for assignments satisfying these constraints and uses demand-proportional ordering to guide its search.

Example Campus Route

An example route evaluated by the current system is:

Start: Boys Hostel

Destination: Main Gate

Reported path:

Boys Hostel
    ↓
Food Court
    ↓
Parking
    ↓
Main Gate


Reported baseline graph cost: 12.50

This number is a graph-cost value, not a verified measurement in seconds or minutes.

The selected path and cost depend on the current campus graph and its edge weights.

Traffic Signal Scheduling

The traffic scheduling component evaluates the following configured demand values:

Junction	NS demand	EW demand
J1	80	40
J2	30	75
J3	65	45
J4	25	90

Demand values are model inputs and should not be interpreted as observed traffic counts unless supported by real data.

The CSP produces feasible signal timings under the current cycle and minimum-green constraints. The evaluator then estimates signal waiting times using a simplified fixed-cycle model.

A complete signal optimization system would additionally need:

A documented mapping between each junction and the road edges that pass through it.
Defined road-cost units, such as seconds or minutes.
A network-level objective based on expected travel time, delay, or queue length.
Comparable baseline and optimized simulations using the same trips and demand assumptions.
Tests that verify the objective improves under the chosen simulation scenario.
Current Limitations

The following features are not yet fully implemented or verified.

Dynamic Signal-Aware Routing

Signal waits are not yet consistently incorporated into road-edge costs. Junction-to-edge mappings and compatible cost units are required before claiming that A* minimizes signal-adjusted travel time.

Average Travel Time Before and After Optimization

The current evaluator can compare theoretical signal-wait estimates and calculate graph costs for selected trips. It does not yet provide a fully integrated, validated comparison of average total travel time before and after CSP optimization across a simulated network.

Incident Management

The following rule-based behaviors are planned but are not yet demonstrated as fully integrated features:

Accident(edge) -> Blocked(edge)
Rain AND Night -> SpeedFactor(0.7)
EmergencyVehicle(vehicle) -> GreenCorridor(route(vehicle))

These rules would need to update the graph or its edge costs and trigger route recalculation.

Probabilistic and Time-Dependent Congestion

The current implementation does not yet establish a complete probabilistic congestion model or prove minimum expected travel time under time-dependent conditions.

Fairness and Restricted Zones

Avoiding school or residential zones has not yet been integrated and verified as a routing constraint or penalty.

Real-World Deployment

The project does not currently use live traffic feeds, deployed traffic controllers, or measured campus travel-time data. It is a prototype intended for algorithmic demonstration and further development.

Future Improvements

Potential next steps include:

Integrate CSP-generated signal timings with the weighted road graph.
Add explicit junction-to-road mappings.
Define consistent travel-time units for road edges.
Implement accident, weather, and emergency-vehicle rules.
Add time-dependent and probabilistic edge costs.
Replan routes when edge availability or costs change.
Simulate multiple trips under identical demand scenarios.
Compare average total travel time before and after optimization.
Extend the test suite to cover dynamic routing, CSP feasibility, and simulation results.
Introduce fairness constraints for sensitive zones.
Add experiment logs and reproducible evaluation settings.
Responsible AI Considerations

A traffic-management system can affect pedestrians, commuters, emergency services, and residents. A future implementation should account for these concerns.

Fairness

Routing policies should avoid shifting excessive traffic into residential streets or sensitive areas merely to reduce travel time for other users.

Privacy

If GPS or location histories are introduced, collect only the information needed for the stated purpose, restrict access, and establish clear retention and deletion policies.

Safety

Signal timings must respect pedestrian crossing requirements and conflicting-movement safety constraints. A software simulation alone is not sufficient to authorize deployment on real roads.

Transparency

The system should explain its route choices, identify important cost assumptions, and distinguish simulated results from measured performance.

Governance

Real-world traffic-control deployment would require appropriate engineering validation, operational oversight, and compliance with relevant transportation regulations.

License

See the LICENSE file for the licensing terms applicable to this project.

Author

Dhanush

GitHub repository: https://github.com/dhanush-3579/rootnavigationAstar

This project is an academic prototype. Its current results demonstrate selected graph-search and CSP scheduling capabilities; full dynamic traffic integration and network-level travel-time optimization remain future work.