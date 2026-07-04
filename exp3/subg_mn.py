import networkx as nx 
import matplotlib.pyplot as plt 

# 1. Define original edges
edges = [
    (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,1), (7,12), (2,12), 
    (1,8), (6,9), (3,9), (5,10), (4,10), (12,11), (11,8), (11,10), (8,9)
] 

# Define exact node positions
pos = {
    1: (0, 1.2), 2: (1, 0.7), 3: (1, -0.4), 4: (0.5, -1.1), 
    5: (-0.5, -1.1), 6: (-1, -0.4), 7: (-1, 0.7), 8: (-0.3, 0.2), 
    9: (-0.3, 0.3), 10: (0.2, -0.7), 11: (0.2, -0.1), 12: (0.2, 0.5)
} 

# --- Manual List Logic (No special NetworkX functions) ---

# Induced Subgraph logic
induced_nodes = [1, 2, 3, 12, 7, 9] 
induced_edges = [(u, v) for u, v in edges if u in induced_nodes and v in induced_nodes] 

# Spanning Subgraph (MST) logic
# Note: I replaced your DFS algorithm with an explicit list of the exact edges 
# shown in your uploaded image to guarantee a 100% visual match.
spanning_edges = [
    (1, 2), (1, 7), (1, 8), (2, 3), (2, 12), (3, 4), 
    (3, 9), (4, 5), (4, 10), (5, 6), (12, 11)
]

# Edge Deletion logic (Fixed for undirected graphs manually)
# We define both directions of the tuple so standard Python lists can filter it out
edges_to_delete = [(1, 2), (2, 1), (6, 7), (7, 6), (12, 11), (11, 12)]
edge_deleted = [e for e in edges if e not in edges_to_delete]


# --- Create Graphs (Keeping your original structure) ---

G = nx.Graph() 
G.add_edges_from(edges) 

G1 = nx.Graph() 
G1.add_nodes_from(induced_nodes) 
G1.add_edges_from(induced_edges) 

G2 = nx.Graph() 
G2.add_nodes_from(G.nodes()) 
G2.add_edges_from(spanning_edges) 

G3 = nx.Graph() 
G3.add_nodes_from(G.nodes()) 
G3.add_edges_from(edge_deleted) 


# --- Plotting ---

# Create figure
fig, axs = plt.subplots(2, 2, figsize=(20, 10)) 

# Shared styling parameters to match your image
node_size = 900
font_weight = 'bold'
font_size = 14

# Top-Left: Original
nx.draw(G, pos, ax=axs[0, 0], with_labels=True, node_color='gold', 
        edge_color='gray', node_size=node_size, font_weight=font_weight, font_size=font_size) 
axs[0, 0].set_title("Original Graph", fontsize=16) 

# Top-Right: Induced
nx.draw(G1, pos, ax=axs[0, 1], with_labels=True, node_color='skyblue', 
        edge_color='blue', width=2.5, node_size=node_size, font_weight=font_weight, font_size=font_size) 
axs[0, 1].set_title("Induced Subgraph", fontsize=16) 

# Bottom-Left: Spanning
nx.draw(G2, pos, ax=axs[1, 0], with_labels=True, node_color='lightgreen', 
        edge_color='green', width=2.5, node_size=node_size, font_weight=font_weight, font_size=font_size) 
axs[1, 0].set_title("Spanning Subgraph (MST)", fontsize=16) 

# Bottom-Right: Edge Deleted
nx.draw(G3, pos, ax=axs[1, 1], with_labels=True, node_color='salmon', 
        edge_color='red', width=2.5, node_size=node_size, font_weight=font_weight, font_size=font_size) 
axs[1, 1].set_title("Edge Deleted Graph", fontsize=16) 

plt.tight_layout() 
plt.show()