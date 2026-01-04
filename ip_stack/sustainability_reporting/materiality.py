class MaterialityReporter:
    """IFRS S2 & CSRD Double Materiality Engine."""
    def calculate_social_value(self, prevented_cases, cost_per_case):
        # Inside-Out Impact: Monetized Health Savings
        return prevented_cases * cost_per_case

    def outside_in_risk(self, climate_volatility):
        # Financial impact of climate on Nairobi Hub operations
        return f"Operational Risk Level: {climate_volatility}"
