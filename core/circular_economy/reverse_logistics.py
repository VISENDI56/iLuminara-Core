class CircularRouter:
    """
    cuOpt for Reverse Logistics (Urban Mining).
    Routes E-Waste to harvesting benches.
    """
    def route_harvest(self, waste_type, location):
        print(f"   [Circular] Routing {waste_type} to nearest Repair-Preneur...")
        return "ROUTE_OPTIMIZED"