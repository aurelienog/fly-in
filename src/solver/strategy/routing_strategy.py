from dataclasses import dataclass

@dataclass
class RoutingStrategy:

    def plan(...):
        pass

class DijkstraStrategy(RoutingStrategy):


class AStarStrategy(RoutingStrategy):
    

class CBSStrategy(RoutingStrategy):