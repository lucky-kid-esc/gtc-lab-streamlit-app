import networkx as nx
import matplotlib.pyplot as plt
import math
def create_graphs():
    G4 = nx.Graph()
    edges4 = [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), 
        (1, 3), (3, 5), (6, 4), (6, 2),                 
        (7, 1), (7, 2), (7, 4), (7, 5)                  
    ]
    G4.add_edges_from(edges4)   
    pos4 = {
        1: (-0.5, math.sqrt(3)/2),  
        2: (0.5, math.sqrt(3)/2),   
        3: (1.0, 0),                
        4: (0.5, -math.sqrt(3)/2),  
        5: (-0.5, -math.sqrt(3)/2), 
        6: (-1.0, 0),               
        7: (0.0, 0)                 
    }
    G5 = nx.Graph()
    nodes5 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    edges5 = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), 
        ('E', 'F'), ('F', 'G'), ('G', 'A'),             
        ('A', 'D'), ('B', 'E'), ('C', 'F'), ('D', 'G'), 
        ('E', 'A'), ('F', 'B'), ('G', 'C')              
    ]
    G5.add_nodes_from(nodes5)
    G5.add_edges_from(edges5)   
    pos5 = {}
    for i, node in enumerate(nodes5):
        theta = math.pi / 2 - i * (2 * math.pi / 7)
        pos5[node] = (math.cos(theta), math.sin(theta))
    return G4, pos4, G5, pos5
def get_cycle_girth(G):
    cycles = nx.cycle_basis(G)
    if not cycles:
        return 0
    return min(len(cycle) for cycle in cycles)
def print_graph_stats(G, name):
    vertices = G.number_of_nodes()
    edges = G.number_of_edges()
    degree_sequence = sorted([d for n, d in G.degree()])
    girth = get_cycle_girth(G)
    print(f"Graph {name}")
    print(f"Vertices         : {vertices}")
    print(f"Edges            : {edges}")
    print(f"Degree Sequence  : {degree_sequence}")
    print(f"Cycle Girth      : {girth}\n")
def main():
    G4, pos4, G5, pos5 = create_graphs()
    print_graph_stats(G4, "G4")
    print_graph_stats(G5, "G5")
    GM = nx.isomorphism.GraphMatcher(G4, G5)
    print("Isomorphism Check:")
    if GM.is_isomorphic():
        print("Result: The graphs are isomorphic.")
    else:
        print("Result: The graphs are NOT isomorphic.")
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    nx.draw(
        G4, pos=pos4, ax=ax[0], with_labels=True, node_color='maroon',
        font_color='white', font_size=16, font_weight='bold', 
        node_size=1200, edge_color='black', width=2.5
    )
    ax[0].set_title("Graph G4", fontsize=18, fontweight='bold', pad=20)
    ax[0].margins(0.15) 
    nx.draw(
        G5, pos=pos5, ax=ax[1], with_labels=True, node_color='maroon',
        font_color='white', font_size=16, font_weight='bold', 
        node_size=1200, edge_color='black', width=2.5
    )
    ax[1].set_title("Graph G5", fontsize=18, fontweight='bold', pad=20)
    ax[1].margins(0.15) 
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()