import matplotlib.pyplot as plt
import networkx as nx
class DSU:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}        
    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]        
    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False
def visualize_mst_only(nodes, edges, pos):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)        
    edges.sort(key=lambda x: x[2])
    dsu = DSU(nodes)
    mst_edges = []
    total_cost = 0
    steps_to_show = len(nodes) - 1
    cols = 4
    rows = (steps_to_show + cols - 1) // cols   
    fig, axes = plt.subplots(rows, cols, figsize=(18, 4 * rows), constrained_layout=True)
    axes = axes.flatten()
    plot_idx = 0   
    for u, v, weight in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v))
            total_cost += weight
            ax = axes[plot_idx]
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', edgecolors='black', node_size=400, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='lightgray', width=1, style='dashed', ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=4, ax=ax)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)           
            ax.set_title(f"Step {plot_idx+1}: Added {u}-{v} (w:{weight})\nTotal Cost: {total_cost}", fontsize=11)
            ax.axis('off')
            plot_idx += 1
            if plot_idx == steps_to_show:
                break
    for j in range(plot_idx, len(axes)):
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
    visualize_mst_only(graph_nodes, graph_edges, graph_pos)