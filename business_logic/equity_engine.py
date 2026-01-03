class ResourceAllocator:
    """
        Resource Allocation with WFP Vulnerability Index Weighting.
            Implements 'Constraint Management'.
                """
                    def calculate_distribution(self, supplies, population_segments):
                            """
                                    supplies: Total vaccines/food units
                                        population_segments: List of dicts {'id': str, 'wfp_score': 0.0-1.0}
                                            """
                                                    # 1. Calculate Weighted Demand
                                                            total_weight = sum([p['wfp_score'] for p in population_segments])
                                                                    
                                                                            allocation_plan = {}
                                                                                    for p in population_segments:
                                                                                            # 2. Distribute based on Vulnerability Ratio
                                                                                                    share = (p['wfp_score'] / total_weight) * supplies
                                                                                                            
                                                                                                                    # 3. Apply Golden Rule Constraint
                                                                                                                            if share < 1.0 and p['wfp_score'] > 0.8:
                                                                                                                                    print(f"⚠️ ALLOCATION ALERT: High vulnerability segment {p['id']} under-served.")
                                                                                                                                            share = max(share, 5.0) # Emergency floor
                                                                                                                                                    
                                                                                                                                                            allocation_plan[p['id']] = share
                                                                                                                                                                    
                                                                                                                                                                            return allocation_plan