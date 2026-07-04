import matplotlib.pyplot as plt
import networkx as nx
def visualize_kruskal_nx(nodes, edges, pos):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    edges.sort(key=lambda x: x[2])    
    MST_G = nx.Graph()
    MST_G.add_nodes_from(nodes)  
    mst_edges = []
    rejected_edges = []
    total_cost = 0
    fig, axes = plt.subplots(4, 4, figsize=(18, 15), constrained_layout=True)
    axes = axes.flatten()   
    for i, (u, v, weight) in enumerate(edges):
        ax = axes[i]
        is_added = False
        if not nx.has_path(MST_G, u, v):
            MST_G.add_edge(u, v, weight=weight)
            mst_edges.append((u, v))
            total_cost += weight
            is_added = True
        else:
            rejected_edges.append((u, v))
        components = list(nx.connected_components(MST_G))
        color_map = {}
        for idx, comp in enumerate(components):
            for node in comp:
                color_map[node] = idx
        node_colors = [color_map[node] for node in nodes]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.Pastel1, 
                               edgecolors='black', node_size=400, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='lightgray', 
                               width=1, style='dashed', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=rejected_edges, edge_color='red', width=1, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=4, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)        
        status = "ADDED" if is_added else "REJECTED"
        ax.set_title(f"Step {i+1}: {u}-{v} (w:{weight})\n{status} | Total Cost: {total_cost}", fontsize=11)
        ax.axis('off')
    for j in range(len(edges), len(axes)):
        axes[j].axis('off')
        
    plt.suptitle("Kruskal's Algorithm:", fontsize=20, fontweight='bold')
    plt.show()
graph_nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
graph_edges = [
    ('A', 'B', 5), ('A', 'C', 10), ('A', 'F', 3), ('A', 'G', 6),
    ('B', 'F', 2),
    ('C', 'G', 1), ('C', 'D', 7),
    ('F', 'G', 1),
    ('G', 'D', 5), ('G', 'H', 9),
    ('D', 'E', 3), ('D', 'H', 4),
    ('H', 'E', 4)
]
graph_pos = {
    'A': (1.5, 4), 'B': (0.5, 2.8), 'C': (2.5, 2.5), 'D': (4, 3.5),
    'E': (5, 2.3), 'F': (1, 1), 'G': (2.2, 0.8), 'H': (4, 1)
}
if __name__ == "__main__":
    visualize_kruskal_nx(graph_nodes, graph_edges, graph_pos)