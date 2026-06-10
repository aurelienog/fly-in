*This project has been created as part of the 42 curriculum by aunoguei.*

# FLY-IN

## Description

This project is a space-time simulation of multiple drones navigating through a network of interconnected hubs.

The system models a graph-based world where:
- **Nodes (hubs)** represent spatial locations with constraints
- **Edges (connections)** represent bidirectional links with capacity limits
- **Drones** are agents that must travel from a start hub to a target hub

### Objective

Compute **collision-free paths for multiple drones** while respecting:

- Node capacity constraints (maximum drones per hub per timestep)
- Edge capacity constraints (maximum drones per connection per timestep)
- Temporal constraints (avoiding space-time collisions)

### Architecture Overview

The project is organized as a pipeline that transforms a map definition into a complete simulation timeline.

This timeline can then be visualized using different rendering modes.

```text
Map Input
    │
    ▼
Parser & Validation
    │
    ▼
Domain Construction
    │
    ▼
Simulation Engine
(Space-Time A* + Reservations)
    │
    ▼
Simulation Timeline
(list of states per timestep)
    │
    ├──────────────► Terminal Renderer
    │                 • Compact output
    │                 • Detailed output
    │                 • Debug-friendly
    │
    └──────────────► Pygame Renderer
                      • Graph visualization
                      • Animated drones
                      • Playback controls
```
Both renderers consume this timeline without influencing pathfinding or scheduling decisions.

### Visualization Modes

The simulation includes two options:

**Terminal Renderer**  
Displays step-by-step drone movement per timestep.

Example:
```
D0-waypoint1
D0-waypoint2 D1-waypoint1
D0-goal D1-waypoint2
D1-goal
```

**Pygame interactive mode**  
Provides a real-time visualization with:

- Network graph rendering
- Playback controls (play/pause/step)
- Time navigation system

---

## Instructions

### Requirements
- Python 3.10+
- pygame
- pytest

### Installation

Create virtual environment and install dependencies:

```bash
make install
```

Or manually:
```bash
pip install pygame
```

### Execution

Run the simulation with:

```bash
make run MAP=maps/sample.txt RENDER=pygame 
```

Or directly:

```bash
python3 fly_in.py maps/sample.txt visual
```

Render options
- `visual` → terminal renderer
- `pygame` → interactive renderer

### Makefile commands

```
make venv         # Create virtual environment
make install      # Install dependencies in the venv
make run          # Run simulation
make debug        # Debug with pdb
make clean        # Remove caches
make clean-venv   # Remove venv
make lint         # Run flake8 + mypy
make lint-strict  # Strict type checking
```

## Algorithm & Implementation Strategy

### 1. Parsing pipeline

#### A. Tokenization

Input file is converted into:

```text
(line_number, keyword, content)
```

Comments and empty lines are ignored.

#### B. Parsing

Entities are parsed independently:
- hubs
- connections
- number of drones
- Metadata ```[key=value]``` syntax

#### C. Validation layer

Ensures:
- Unique hub names and coordinates
- Exactly one start hub and one end hub
- Valid metadata: zones, colors, capacities
- Valid connections (no duplicates, no self-loops)
- Reachability from start to end

#### D. Domain construction

Raw input is transformed into domain objects:
- Network
- Hub
- Connection
- Drone

### 2. Pathfinding algorithm (core logic)

The routing system uses a Space-Time A* algorithm:

**State representation**

A state is defined as: ```(hub, timestep)```

This enables:
- Movement over time
- Waiting actions
- Collision avoidance

**Search strategy**

- A* search over a time-expanded graph
- Priority queue ordered by f = g + h
- Heuristic based on Euclidean distance

**Constraints**

At each step:
- Node capacity limits
- Edge capacity limits
- Zone restrictions (blocked / priority / cost modifiers)

**Reservation system**

A global Reservation Table prevents collisions:

- ```node_reservations```: occupancy per (hub, timestep)
- ```edge_reservations```: occupancy per (connection, time interval)

Once a drone path is computed, it is immediately reserved, making later drones aware of earlier ones.

**Scheduling strategy**

Drones are processed sequentially:

1. Compute path with A*
2. Reserve path in time-space
3. Repeat for next drone

This produces a greedy prioritized multi-agent schedule.

### 3. Cost model design

Routing costs are centralized in CostModel, which defines:

- Euclidean distance
- Movement cost
- Congestion penalty
- Zone modifiers

Cost logic is decoupled from the planner to allow experimentation without modifying A*.

## Performance, Scalability

### Complexity

- Each drone runs A*
- Total cost scales linearly with number of drones
- State space grows with time horizon

### Works well when:

- Sparse graphs
- Moderate drone count (tens–low hundreds)
- Low congestion

### Degrades when:
- High contention on hubs/edges
- Dense graphs
- Long time horizons

### Limitation

Because the system is **sequentially greedy**, later drones may experience:
- longer paths
- increased waiting times
- higher computational cost due to congestion

More advanced alternatives:

- CBS (Conflict-Based Search)
- WHCA*
- Parallel multi-agent planning

### Caching Strategy

❌ No global path caching  
✔️ Reservation table acts as implicit memory

Stored:
- Node occupancy over time
- Edge occupancy over time

Recomputed:
- Full A* per drone

## Rendering System

The visualization layer is designed to improve understanding of the simulation by making it possible to observe:
- A* search behavior (indirectly through movement patterns)
- Scheduling decisions between drones
- Congestion dynamics
- Emergent routing inefficiencies

The project supports **two distinct rendering modes**:
- **Terminal renderer (CLI)**
- **Pygame interactive renderer (GUI)**

Both visualize the same simulation state, but with different levels of detail and interactivity.

### Terminal Renderer

The terminal renderer provides a **step-by-step textual simulation trace**.

Each timestep is printed as a single line, showing all drone movements at that moment.

Each movement must follow the format: ```D<ID>-<zone>, or D<ID>-<connection>```

**Output format:**

By default, a simplified representation is used:
```
D<ID>-<hub>
D<ID>-<connection>
````
Example:
```
D0-waypoint1
D0-waypoint2 D1-waypoint1
D0-goal D1-waypoint2
D1-goal
```

A more detailed and colored representation is printed with: ``` make run RENDER=visual``` or ```fly_in.py maps/sample.txt visual```

Representation:
T<turn-number>: D<ID>-<zone> <occupation/capacity>, or D<ID>-<connection><occupation/capacity>

Example:
```
T001: D0-waypoint1<1/1>
T002: D0-waypoint2<1/1> D1-waypoint1<1/1>
T003: D0-goal<1/1> D1-waypoint2<1/1>
T004: D1-goal<1/1>
```

### Pygame Renderer

**1. World rendering**

The simulation world is drawn as a graph:

- ```Hubs``` as colored circles
- ```Connections``` as edges between hubs
- ```Drones``` as animated agents moving along planned paths

**2. Camera system**

The camera supports:

- Panning (center adjustment)
- Zooming
- World-to-screen coordinate transformation

At startup, the camera automatically:

- Computes graph bounding box
- Fits the entire network into view

**3. UI overlay**

A side panel provides:

- Simulation status (play/pause)
- Current timestep / max timestep
- Network statistics
- Drone completion tracking
- Keyboard controls legend

## Controls

The simulation can be paused to manually inspect each timestep:

```
SPACE → Play/Pause
LEFT  → Previous step
RIGHT → Next step
Q     → Zoom in
E     → Zoom out
```

Both renderers share the same simulation core but differ in how the state is presented.

## Technical Summary

**Key design decisions:**
- Separation of parsing and domain model
- Strong validation layer before construction
- Centralized cost model abstraction
- Sequential scheduling with reservation propagation

**Future improvements (optional extensions)**
- Parallel multi-agent planning (CBS or WHCA*)
- Path re-planning under dynamic obstacles
- GPU-based rendering optimization

## Resources

### Graphs & algorithms

- https://www.geeksforgeeks.org/dsa/graph-data-structure-and-algorithms/
- https://www.geeksforgeeks.org/dsa/a-search-algorithm/
- https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/

### Python
- https://docs.python.org/3/library/dataclasses.html

### Visualization
- https://www.pygame.org/docs/

### Videos
- https://www.youtube.com/watch?v=4jyESQDrpls
- https://www.youtube.com/watch?v=UeZR3IzVbwM

### AI usage

Artificial intelligence was used to assist with:

- Documentation structure and clarity
- Docstring standardization (PEP 257)
- Explanation of Space-Time A* and reservation system
- Refactoring suggestions (separation of concerns)