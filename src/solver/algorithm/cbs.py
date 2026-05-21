Multi-agent coordinator.

Usa A* internamente.

Flow:

CBS
 ├── Drone1 → A*
 ├── Drone2 → A*
 ├── Drone3 → A*
        ↓
detect conflict
        ↓
add constraint
        ↓
replan