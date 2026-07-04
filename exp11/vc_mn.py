import networkx as nx
import matplotlib.pyplot as plt
import random
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges = [
    ('A', 'B'), ('A', 'F'), ('A', 'G'), 
    ('B', 'C'), ('B', 'F'), 
    ('C', 'D'), ('C', 'E'), ('C', 'F'), 
    ('D', 'E'), 
    ('E', 'F'), ('E', 'G'), 
    ('F', 'G')
]
def custom_greedy_color(nodes, edges, shuffle=False):
    adj_list = {node: [] for node in nodes}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)        
    process_order = list(nodes)
    if shuffle: 
        random.shuffle(process_order)        
    coloring = {}
    for node in process_order:
        used_colors = set()
        for neighbor in adj_list[node]:
            if neighbor in coloring: 
                used_colors.add(coloring[neighbor])
        color = 0
        while color in used_colors: 
            color += 1            
        coloring[node] = color        
    return coloring
coloring = custom_greedy_color(nodes, edges, shuffle=False)
colors = ["red", "blue", "green", "yellow", "orange", "pink"]
print("Vertex Colors:")
for node in sorted(coloring.keys()): 
    print(f"Vertex {node} ---> Color {colors[coloring[node]][0].upper()}")
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
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
plt.title("Graph Coloring")
plt.show()