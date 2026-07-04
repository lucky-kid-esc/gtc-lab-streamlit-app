import networkx as nx 
import matplotlib.pyplot as plt 
G = nx.Graph() 
edges = [ 
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), 
    (7, 12), (2, 12), (1, 8), (6, 9), (3, 9), (5, 10), (4, 10), 
    (12, 11), (11, 8), (11, 10), (8, 9) 
] 
G.add_edges_from(edges) 
pos = { 
    1: (0, 1.2), 2: (1, 0.7), 3: (1, -0.4), 4: (0.5, -1.1), 
    5: (-0.5, -1.1), 6: (-1, -0.4), 7: (-1, 0.7), 8: (-0.3, 0.2), 
    9: (-0.3, -0.3), 10: (0.2, -0.7), 11: (0.2, -0.1), 12: (0.2, 0.5) 
} 
induced_nodes = [1, 2, 3, 12, 7, 9] 
G_induced = G.subgraph(induced_nodes) 
G_spanning = nx.minimum_spanning_tree(G) 
G_edge_deleted = G.copy() 
G_edge_deleted.remove_edges_from([(1, 2), (6, 7), (12, 11)]) 
fig, axs = plt.subplots(2, 2, figsize=(12, 12)) 
nx.draw(G, pos, ax=axs[0, 0], with_labels=True, node_color='gold',  
        node_size=600, font_weight='bold', edge_color='gray') 
axs[0, 0].set_title("Original Graph") 
nx.draw(G_induced, pos, ax=axs[0, 1], with_labels=True, node_color='skyblue',  
        node_size=600, font_weight='bold', edge_color='blue', width=2) 
axs[0, 1].set_title("Induced Subgraph ") 
nx.draw(G_spanning, pos, ax=axs[1, 0], with_labels=True, node_color='lightgreen',  
        node_size=600, font_weight='bold', edge_color='green', width=2) 
axs[1, 0].set_title("Spanning Subgraph (MST)") 
 
nx.draw(G_edge_deleted, pos, ax=axs[1, 1], with_labels=True, node_color='salmon',  
        node_size=600, font_weight='bold', edge_color='red', width=2) 
axs[1, 1].set_title("Edge Deleted Graph") 
plt.tight_layout() 
plt.show() 