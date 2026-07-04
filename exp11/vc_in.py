import networkx as nx
import matplotlib.pyplot as plt
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges = [
    ('A', 'B'), ('A', 'F'), ('A', 'G'), 
    ('B', 'C'), ('B', 'F'), 
    ('C', 'D'), ('C', 'E'), ('C', 'F'), 
    ('D', 'E'), 
    ('E', 'F'), ('E', 'G'), 
    ('F', 'G')
]
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
coloring = nx.coloring.greedy_color(G, strategy=lambda *args: ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
colors = ["red", "blue", "green", "yellow", "orange", "pink"]
print("Vertex Colors:")
for node in sorted(coloring.keys()): 
    print(f"Vertex {node} ---> Color {colors[coloring[node]][0].upper()}")
color_map = [colors[coloring[node]] for node in G.nodes()]
pos = {
    'A': (0, 1), 
    'B': (1, 2), 
    'C': (3, 2), 
    'D': (4, 1), 
    'E': (3, 0), 
    'F': (1.5, 1), 
    'G': (1, 0)
}
plt.figure(figsize=(8, 6))
nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_color=color_map, 
    node_size=1200, 
    font_size=12, 
    font_color="white", 
    font_weight="bold", 
    edge_color="gray"
)
edge_weights = {
    ('A', 'B'): 12, ('A', 'F'): 16, ('A', 'G'): 14, 
    ('B', 'C'): 10, ('B', 'F'): 7, 
    ('C', 'D'): 3, ('C', 'E'): 5, ('C', 'F'): 6, 
    ('D', 'E'): 4, 
    ('E', 'F'): 2, ('E', 'G'): 8, 
    ('F', 'G'): 9
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_size=10)
plt.title("Graph Coloring (NetworkX Alphabetical)")
plt.show()