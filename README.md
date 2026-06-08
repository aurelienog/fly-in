*This project has been created as part of the 42 curriculum by aunoguei.*

# FLY-IN

## Description

This project is a space-time simulation of multiple drones navigating through a network of interconnected hubs.

The system models a graph-based world where:
- Nodes represent hubs with spatial coordinates and movement constraints
- Edges represent bidirectional connections with capacity limits
- Drones are agents that must travel from a start hub to a target hub

The main objective is to compute **collision-free paths for multiple drones** while respecting:
- Node capacity constraints (maximum drones per hub)
- Edge capacity constraints (maximum drones per connection per timestep)
- Temporal constraints (space-time collisions)

The simulation includes a full visualization layer built with Pygame, showing:
- Network structure
- Drone movement over time
- Animated transitions between hubs
- A playback system with time controls

---

## Instructions
 about compilation,
installation, and/or execution.
### Requirements
- Python 3.10+
- pygame
- pytest

Install dependencies:

```bash
pip install pygame
```
### Running the simulation

Run the project by providing a map file:
python3 main.py <map_file>

Example:
```bash
python3 main.py maps/sample.txt
```

## Algorithm & Implementation Strategy

### 1. Parsing pipeline

The input file is processed in multiple stages:

#### A. Tokenization
Lines are converted into ```(line_number, keyword,content)``` tokens

Comments and empty lines are ignored

#### B. Parsing

Each entity type is parsed independently:
- hubs
- connections
- number of drones
- Metadata is extracted using bracket-based parsing ```[key=value]```

#### C. Validation layer

The system enforces:
- Unique hub names
- Unique coordinates
- Exactly one start hub and one end hub
- Valid zones, colors, and capacities
- Valid connections (no duplicates, no self-loops)
- Reachability between start and end

#### D. Domain construction

Raw data is converted into domain objects:
- Network
- Hub
- Connection
- Drone

### 2. Pathfinding algorithm (core logic)

The routing system uses a Space-Time A* algorithm:

**State representation**

A state is defined as: ```(hub, timestep)```

This allows modeling:

- movement over time
- waiting actions
- collision avoidance

**Search strategy**

The algorithm uses:

- A* search over a time-expanded graph
- Priority queue ordered by f = g + h
- Heuristic based on Euclidean distance

**Constraints enforced**

At each expansion step:

- Node constraint:
- max drones per hub per timestep
- Edge constraint:
- max link capacity per timestep interval
- Zone constraints:
- blocked hubs are not traversable
- restricted zones increase cost
- priority zones reduce cost

**Reservation system**

A global ReservationTable is used to prevent conflicts:

- ```node_reservations```: occupancy per (hub, timestep)
- ```edge_reservations```: occupancy per (connection, time interval)

Once a drone path is computed, it is immediately reserved, making later drones aware of earlier ones.

**Scheduling strategy**

Drones are processed sequentially:

1. Plan path with A*
2. Reserve path in time-space
3. Repeat for next drone

This produces a greedy prioritized multi-agent schedule.


### 3. Cost model design

Routing costs are centralized in CostModel, which defines:

- geometric distance
- hub movement cost
- congestion penalty
- zone modifiers

This avoids coupling pathfinding logic with heuristic tuning.

Key design choice:

>Cost computation is fully separated from the planner to allow experimentation without modifying A* logic.

## Performance, Scalability & Complexity Analysis

### How efficient is the algorithm?

The core algorithm is a **Space-Time A\*** planner combined with a **reservation-based scheduling system**.

Efficiency depends mainly on:
- number of hubs
- number of connections
- time horizon explored
- number of drones

Each drone is planned sequentially using A*, so the total cost scales linearly with the number of agents, but each search is constrained by previously reserved paths.

### Can it scale to a large number of drones?

Yes, but with important constraints:

#### Works well when:
- sparse graph (low connection density)
- moderate number of drones (tens to low hundreds)
- short-to-medium time horizons
- limited congestion

#### Degrades when:
- many drones compete for same hubs/edges
- dense graphs increase branching factor
- long time horizons expand state space
- high contention forces repeated re-routing

Because the system is **sequentially greedy**, later drones may experience:
- longer paths
- increased waiting times
- higher computational cost due to congestion

A fully optimal multi-agent solution would require:
- CBS (Conflict-Based Search), or
- WHCA*, or
- parallel planning strategies

### Are paths recalculated or cached?

- Paths are **NOT globally cached**
- Each drone is planned independently
- However, the system uses a **reservation table as implicit state memory**

#### What is cached:
- Node occupancy over time
- Edge occupancy over time

#### What is recalculated:
- Full A* search per drone
- No reuse of previous shortest-path trees

This design prioritizes:
> correctness under constraints over global optimal reuse

## Visualization Features

The visualization layer significantly improves understanding of the simulation. It transforms an abstract algorithm into:

> a **human-readable space-time system**

making it possible to observe:
- A* search behavior indirectly
- scheduling decisions
- congestion dynamics
- emergent routing inefficiencies

This is especially valuable for debugging multi-agent pathfinding systems, where correctness is not enough without interpretability.

The project includes a real-time visualization engine using Pygame. ANNNNNNNND TODO

**1. World rendering**

The renderer displays:

- ```Hubs``` as colored circles
- ```Connections``` as edges between hubs
- ```Drones``` as moving entities with interpolation

**2. Camera system**

The camera supports:

- Panning (center adjustment)
- Zooming
- World-to-screen transformation

It automatically fits the graph at startup using bounding box normalization.

**3. UI overlay**

A side panel provides:

- Simulation status (play/pause)
- Current timestep / max timestep
- Network statistics
- Drone completion tracking
- Keyboard controls legend

## Technical Summary

**Key design decisions: **
- Separation of raw parsing vs domain model
- Strong validation layer before construction
- Centralized cost model abstraction
- Sequential scheduling with reservation propagation

**Future improvements (optional extensions)**
- Parallel multi-agent planning (CBS or WHCA*)
- Path re-planning under dynamic obstacles
- GPU-based rendering optimization

## Resources

Algorithms & theory
A* Search Algorithm:
https://en.wikipedia.org/wiki/A*_search_algorithm
Multi-Agent Pathfinding (MAPF):
https://movingai.com/benchmarks/mapf.html
Space-time planning concepts:
https://doi.org/10.1109/ICRA.2019.8794223

### Pygame documentation
https://www.pygame.org/docs/

### Python references
Dataclasses:
https://docs.python.org/3/library/dataclasses.html

### AI usage disclosure

Artificial intelligence was used in the following parts of this project:

- Writing and refining documentation (README structure and clarity)
- Generating and standardizing docstrings across modules (PEP 257 compliance)
- Improving explanations of algorithm design (Space-Time A*, reservation system)
- Assisting with refactoring suggestions for separation of concerns (rendering vs logic)