import matplotlib.pyplot as plt 
import networkx as nx 
from collections import Counter

def create_graphs(): 
    G1, G2 = nx.Graph(), nx.Graph() 
    e1 = [ 
        ("V1","V2"), ("V1","V4"), ("V1","V5"), ("V1","V3"), 
        ("V2","V4"), ("V2","V6"), ("V6","V3"), ("V5","V6")    
    ] 
    e2 = [ 
        ("V1","V2"), ("V1","V3"), ("V2","V4"), ("V3","V4"), 
        ("V4","V5"), ("V4","V6"), ("V5","V6")    
    ] 
    G1.add_edges_from(e1) 
    G2.add_edges_from(e2) 
    
    pos1 = { 
        "V1": (-2, 0), "V2": (0, 2), "V3": (3, 0.5), 
        "V4": (-0.5, -0.3), "V5": (-2, -2), "V6": (1.5, -1.5)    
    } 
    pos2 = { 
        "V1": (0, 2), "V2": (-1.5, 1), "V3": (1.5, 1), 
        "V4": (0, 0), "V5": (-1.5, -1.5), "V6": (1.5, -1.5)    
    }
    
    return (G1, pos1), (G2, pos2) 

def find_closed_path(G, start, curr=None, visited=None, path=None): 
    if curr is None: curr = start 
    if visited is None: visited = {start} 
    if path is None: path = [start] 
    
    if len(path) >= 5 and G.has_edge(curr, start): 
        return path + [start]     
        
    for n in sorted(list(G.neighbors(curr))): 
        if n not in visited: 
            res = find_closed_path(G, start, n, visited | {n}, path + [n]) 
            if res: return res     
            
    if len(path) >= 3 and G.has_edge(curr, start): 
        return path + [start] 
        
    return None 

def find_closed_trail(G, start, curr=None, visited_edges=None, path=None): 
    if curr is None: curr = start 
    if visited_edges is None: visited_edges = set() 
    if path is None: path = [start] 
    
    if len(path) >= 8 and G.has_edge(curr, start): 
        edge_to_start = tuple(sorted((curr, start))) 
        if edge_to_start not in visited_edges: 
            return path + [start]         
            
    for n in sorted(list(G.neighbors(curr))): 
        edge = tuple(sorted((curr, n))) 
        if edge not in visited_edges: 
            res = find_closed_trail( 
                G, start, n, 
                visited_edges | {edge}, 
                path + [n]            
            ) 
            if res: return res             
            
    if len(path) >= 3 and G.has_edge(curr, start): 
        edge_to_start = tuple(sorted((curr, start))) 
        if edge_to_start not in visited_edges: 
            return path + [start] 
            
    return None 

def find_closed_walk(G, start): 
    path = [start] 
    curr = start 
    
    for i in range(12): 
        neighbors = sorted(list(G.neighbors(curr))) 
        curr = neighbors[(i + 1) % len(neighbors)] 
        path.append(curr)     
        
    for _ in range(10): 
        if G.has_edge(curr, start): 
            path.append(start) 
            return path 
        neighbors = sorted(list(G.neighbors(curr))) 
        curr = neighbors[0] 
        path.append(curr)     
        
    if path[-1] != start: 
        path.append(start) 
        
    return path 

def find_sequence(G, start, type='path'): 
    if type == 'path': 
        return find_closed_path(G, start) 
    if type == 'trail': 
        return find_closed_trail(G, start) 
    if type == 'walk': 
        return find_closed_walk(G, start) 
    return None 

def draw(G, pos, ax, seq, title, color): 
    nx.draw( 
        G, pos, ax=ax, 
        node_color='lightgrey', edge_color='lightgrey', 
        with_labels=True, node_size=900, font_weight='bold'    
    ) 
    
    if seq: 
        edge_list = [tuple(sorted((seq[i], seq[i+1]))) for i in range(len(seq)-1)] 
        counts = Counter(edge_list)        
        
        single_edges = [e for e, c in counts.items() if c == 1] 
        multi_edges = [e for e, c in counts.items() if c > 1]        
        
        nx.draw_networkx_nodes(G, pos, nodelist=seq, ax=ax, node_color=color)        
        nx.draw_networkx_edges(G, pos, edgelist=single_edges, ax=ax, edge_color=color, width=2)        
        
        dark_colors = {'red': 'darkred', 'green': 'darkgreen', 'blue': 'darkblue'} 
        dark_color = dark_colors.get(color, 'black') 
        
        nx.draw_networkx_edges(G, pos, edgelist=multi_edges, ax=ax, edge_color=dark_color, width=5)        
        
    ax.set_title(f"{title}\n{seq}") 

def main(): 
    (G1, p1), (G2, p2) = create_graphs()     
    
    plt.figure(1, figsize=(10,5)) 
    ax1, ax2 = plt.subplot(121), plt.subplot(122) 
    draw(G1, p1, ax1, None, "Original G1", "grey") 
    draw(G2, p2, ax2, None, "Original G2", "grey") 
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), num=2) 
    
    for i, (G, p, name) in enumerate([(G1, p1, "G1"), (G2, p2, "G2")]): 
        start = sorted(list(G.nodes()))[0] 
        draw(G, p, axes[i,0], find_sequence(G, start, 'walk'), f"{name} Walk", "red") 
        draw(G, p, axes[i,1], find_sequence(G, start, 'trail'), f"{name} Trail", "green") 
        draw(G, p, axes[i,2], find_sequence(G, start, 'path'), f"{name} Path", "blue")    
        
    plt.tight_layout() 
    plt.show() 

if __name__ == "__main__": 
    main()