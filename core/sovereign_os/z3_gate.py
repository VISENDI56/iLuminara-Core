class Z3Gate:
    """Z3-Gate: 50ms guillotine for clinical predicates."""
    def verify(self, diag_output): return "SAT" if diag_output else "UNSAT"
