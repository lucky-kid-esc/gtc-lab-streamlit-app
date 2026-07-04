import matplotlib.pyplot as plt
import networkx as nx
def create_graph():
    G = nx.Graph()
    edges = [
        ("V1", "V2"),
        ("V1", "V3"),
        ("V2", "V4"),
        ("V3", "V4"),
        ("V4", "V5"),
        ("V4", "V6"),
        ("V5", "V6"),
        ("V2", "V5")    ]
    G.add_edges_from(edges)
    pos = {
        "V1": (0, 2),
        "V2": (-1.5, 1),
        "V3": (1.5, 1),
        "V4": (0, 0),
        "V5": (-1.5, -1.5),
        "V6": (1.5, -1.5)    }
    return G, pos
def find_hamiltonian_cycle():
    return [
        "V1",
        "V2",
        "V5",
        "V6",
        "V4",
        "V3",
        "V1"    ]
def main():
    G, pos = create_graph()
    cycle = find_hamiltonian_cycle()
    print("Hamiltonian Cycle Found:")
    print(" -> ".join(cycle))
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='lightgreen',
        edge_color='gray',
        node_size=1200,
        font_weight='bold',
        width=2    )
    cycle_edges = [
        (cycle[i], cycle[i+1])
        for i in range(len(cycle)-1)    ]
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=cycle_edges,
        edge_color='red',
        width=4    )
    plt.title(
        "Hamiltonian Cycle\n"
        "V1 → V2 → V5 → V6 → V4 → V3 → V1",
        fontsize=13,
        fontweight='bold'    )
    plt.axis('off')
    plt.show()
if __name__ == "__main__":
    main()