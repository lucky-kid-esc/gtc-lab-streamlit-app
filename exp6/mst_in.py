import matplotlib.pyplot as plt 
import networkx as nx 
def create_graph():
    G = nx.Graph()
    v = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    G.add_nodes_from(v)
    e = [
        ('A', 'B', 5), ('A', 'C', 10), ('A', 'F', 3), ('A', 'G', 6),
        ('B', 'F', 2),
        ('C', 'G', 1), ('C', 'D', 7),
        ('F', 'G', 1),
        ('G', 'D', 5), ('G', 'H', 9),
        ('D', 'E', 3), ('D', 'H', 4),
        ('H', 'E', 4)    ]
    G.add_weighted_edges_from(e)
    return G
def create_mst(G):
    mst = nx.minimum_spanning_tree(G)
    return mst
def main():
    G = create_graph()
    mst = create_mst(G)
    fig, ax = plt.subplots(2, 1, figsize=(10, 12))    
    pos = {
        'A': (1.5, 4),
        'B': (0.5, 2.8),
        'C': (2.5, 2.5),
        'D': (4, 3.5),
        'E': (5, 2.3),
        'F': (1, 1),
        'G': (2.2, 0.8),
        'H': (4, 1)    }
    ax[0].set_title("Original Graph (All Edges)")
    nx.draw(G, ax=ax[0], pos=pos, with_labels=True, node_color='red', edgecolors='black', node_size=800, font_weight='bold')
    edge_labels_G = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_G, ax=ax[0])
    ax[1].set_title("Minimum Spanning Tree (MST)")
    nx.draw(mst, ax=ax[1], pos=pos, with_labels=True, node_color='red', edgecolors='black', node_size=800, font_weight='bold', edge_color='red', width=2)
    edge_labels_mst = nx.get_edge_attributes(mst, "weight")
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=edge_labels_mst, ax=ax[1])
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()