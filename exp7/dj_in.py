import networkx as nx 
import matplotlib.pyplot as plt 
def dijkstra_builtin(edges, pos, start_node): 
    G = nx.Graph() 
    G.add_weighted_edges_from(edges) 
    distances, paths = nx.single_source_dijkstra(G, start_node)     
    print("Shortest Distances:") 
    for node in sorted(distances): 
        print(f"{start_node} -> {node} = {distances[node]}")        
    plt.figure(figsize=(10, 6))     
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
            node_size=1000, font_size=12, font_weight='bold') 
    edge_labels = nx.get_edge_attributes(G, 'weight') 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) 
    path_edges = [] 
    for target in paths: 
        path = paths[target] 
        for i in range(len(path) - 1): 
            path_edges.append((path[i], path[i+1])) 
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3) 
    
    plt.title(f"Built-in Dijkstra from Node {start_node}") 
    plt.axis('off') 
    plt.show() 
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
if __name__ == "__main__":
    dijkstra_builtin(graph_edges, graph_pos, 0)