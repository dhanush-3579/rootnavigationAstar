"""Rule-based incident manager for smart traffic routing."""

class IncidentManager:
    def __init__(self, road_graph):
        self.graph = road_graph
        self.blocked_roads = set()
        self.speed_factor = 1.0
        self.emergency_corridor = []

    def accident(self, source, destination):
        """Accident(source, destination) -> Blocked(edge)."""
        if destination not in self.graph.get(source, {}):
            raise ValueError("Road does not exist.")

        self.blocked_roads.add((source, destination))
        print(f"RULE: Accident on {source} -> {destination}")
        print("ACTION: Road blocked.")

    def set_weather(self, rain=False, night=False):
        """Rain AND Night -> SpeedFactor(0.7)."""
        if rain and night:
            self.speed_factor = 0.7
            print("RULE: Rain AND Night")
            print("ACTION: Speed reduced to 70% of normal.")
        else:
            self.speed_factor = 1.0
            print("ACTION: Normal speed factor restored.")

    def emergency_vehicle(self, route):
        """EmergencyVehicle(vehicle) -> GreenCorridor(route)."""
        if not route or len(route) < 2:
            raise ValueError("Emergency route must contain at least two nodes.")

        for source, destination in zip(route, route[1:]):
            if destination not in self.graph.get(source, {}):
                raise ValueError(
                    f"Invalid road in emergency route: {source} -> {destination}"
                )

        self.emergency_corridor = list(route)
        print("RULE: Emergency vehicle detected.")
        print("ACTION: Priority corridor:", " -> ".join(route))

    def get_updated_graph(self):
        """Return a copy with closures and weather-adjusted travel costs."""
        updated = {}

        for source, neighbours in self.graph.items():
            updated[source] = {}

            for destination, base_cost in neighbours.items():
                if (source, destination) in self.blocked_roads:
                    continue

                # Slower speed means a larger travel time.
                updated[source][destination] = base_cost / self.speed_factor

        # Preserve destination nodes even if they have no outgoing roads.
        return updated
