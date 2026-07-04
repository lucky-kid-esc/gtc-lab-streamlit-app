import networkx as nx 
import matplotlib.pyplot as plt 
from typing import List, Tuple, Dict

def create_graph(edges: List[Tuple[int, int, int]]) -> nx.Graph:
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    return G

def visualize_dijkstra(G: nx.Graph, pos: Dict[int, Tuple[float, float]], start_node: int) -> None:
    try:
        distances, paths = nx.single_source_dijkstra(G, start_node)
    except nx.NetworkXNoPath:
        print(f"Error: Could not compute paths from {start_node}.")
        return

    print(f"--- Shortest Distances from Node {start_node} ---")
    for node in sorted(distances):
        print(f"Path {start_node} -> {node} : Cost = {distances[node]}")

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    
    nx.draw_networkx_nodes(G, pos, node_color='#A0D995', edgecolors='black', node_size=1200, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, style='dashed', alpha=0.7, ax=ax)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, 
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.8), ax=ax)
    
    path_edges = [
        (paths[target][i], paths[target][i+1]) 
        for target in paths for i in range(len(paths[target]) - 1)
    ]
    
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#FF5733', width=3.5, ax=ax)

    ax.set_title(f"Dijkstra's Shortest Path Tree (Source: Node {start_node})", 
                 fontsize=14, fontweight='bold', pad=15)
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    graph_edges = [
        (0, 1, 3), (0, 2, 1), (0, 3, 6),
        (1, 2, 5), (1, 4, 3),
        (2, 3, 5), (2, 4, 6), (2, 5, 4),
        (3, 5, 2),
        (4, 5, 6)
    ]

    graph_pos = {
        0: (1, 2), 1: (0, 1), 2: (1, 0.5), 
        3: (2, 1), 4: (0, -1), 5: (2, -1)
    }

    G = create_graph(graph_edges)
    visualize_dijkstra(G, graph_pos, start_node=0)