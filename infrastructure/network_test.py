import networkx as nx

def verify_graph_engine():
    """Validates that the NetworkX engine can handle iLuminara propagation logic."""
    G = nx.Graph()
    G.add_edge("Edge_Node_Nairobi", "Nexus_Core")
    is_valid = nx.is_connected(G)
    print(f"   [NetworkX] Validation: {'SUCCESS' if is_valid else 'FAILED'}")
    return is_valid

if __name__ == "__main__":
    verify_graph_engine()