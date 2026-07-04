import networkx as nx
import matplotlib.pyplot as plt
import sys
from typing import List, Tuple

def dijkstra_with_visualization(edges: List[Tuple[int, int, int]], start_node: int):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    nodes = sorted(list(G.nodes()))
    n = len(nodes)
    
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    visited = set()
    predecessors = {node: None for node in nodes}
    
    print(f"{'Step':<5} | {'Pick':<5} | {'Distances (Nodes 0 to 5)':<35}")
    print("-" * 55)
    
    step = 1
    
    while len(visited) < n:
        unvisited = [node for node in nodes if node not in visited]
        if not unvisited:
            break
            
        u = min(unvisited, key=lambda x: distances[x])
        
        if distances[u] == float('inf'):
            break
            
        visited.add(u)
        
        for v in G.neighbors(u):
            if v not in visited:
                weight = G[u][v]['weight']
                new_dist = distances[u] + weight
                
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    
        dist_list = [str(distances[node]) if distances[node] != float('inf') else "∞" for node in nodes]
        print(f"{step:<5} | {u:<5} | {str(dist_list):<35}")
        step += 1
        
    pos = {
        0: (1, 2), 1: (0, 1), 2: (1, 0.5), 
        3: (2, 1), 4: (0, -1), 5: (2, -1)
    }
    
    plt.figure(figsize=(10, 6))
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', style='dashed')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    path_edges = []
    for node, pred in predecessors.items():
        if pred is not None:
            path_edges.append((pred, node))
            
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    
    plt.title(f"Manual Dijkstra Result (Source: Node {start_node})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    graph_edges = [
        (0, 1, 3), (0, 2, 1), (0, 3, 6),
        (1, 2, 5), (1, 4, 3),
        (2, 3, 5), (2, 4, 6), (2, 5, 4),
        (3, 5, 2),
        (4, 5, 6)
    ]
    
    dijkstra_with_visualization(graph_edges, start_node=0)