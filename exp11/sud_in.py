import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.Graph()
nodes = [(r, c) for r in range(4) for c in range(4)]
G.add_nodes_from(nodes)

for r in range(4):
    for c in range(4):
        for i in range(4):
            if i != c: 
                G.add_edge((r, c), (r, i))
            if i != r: 
                G.add_edge((r, c), (i, c))
        br, bc = 2 * (r // 2), 2 * (c // 2)
        for i in range(2):
            for j in range(2):
                if (br + i, bc + j) != (r, c):
                    G.add_edge((r, c), (br + i, bc + j))
input_grid = [
    [0, 0, 0, 2],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [1, 0, 0, 0]
]
initial_colors = {
    (r, c): input_grid[r][c] 
    for r in range(4) for c in range(4) 
    if input_grid[r][c] != 0
}
def solve_coloring(graph, node_colors, num_colors=4):
    if len(node_colors) == len(graph.nodes):
        return node_colors    
    uncolored = [n for n in graph.nodes if n not in node_colors]
    uncolored.sort(key=lambda n: len([neighbor for neighbor in graph.neighbors(n) if neighbor in node_colors]), reverse=True)
    node = uncolored[0]    
    for color in range(1, num_colors + 1):
        if all(node_colors.get(neighbor) != color for neighbor in graph.neighbors(node)):
            node_colors[node] = color
            result = solve_coloring(graph, node_colors, num_colors)
            if result:
                return result
            del node_colors[node]
    return None
solution = solve_coloring(G, initial_colors.copy())
pos = {(r, c): (c, -r) for r in range(4) for c in range(4)}
color_map = {1: '#ff9999', 2: '#66b3ff', 3: '#99ff99', 4: '#ffcc99'}
node_colors = [color_map[solution[n]] for n in G.nodes()]
labels = {n: str(solution[n]) for n in G.nodes()}
fig, ax = plt.subplots(figsize=(10, 10))
straight_edges = []
arc_edges = []
for u, v in G.edges():
    r1, c1 = u
    r2, c2 = v    
    if (r1, c1) > (r2, c2):
        r1, c1, r2, c2 = r2, c2, r1, c1
        u, v = (r1, c1), (r2, c2)        
    if r1 == r2 and abs(c1 - c2) > 1:
        dist = abs(c1 - c2)
        mag = 0.3 if dist == 2 else 0.2
        rad = -mag if r1 < 2 else mag
        arc_edges.append((u, v, rad))        
    elif c1 == c2 and abs(r1 - r2) > 1:
        dist = abs(r1 - r2)
        mag = 0.3 if dist == 2 else 0.2
        rad = mag if c1 < 2 else -mag
        arc_edges.append((u, v, rad))        
    else:
        straight_edges.append((u, v))
nx.draw_networkx_edges(G, pos, edgelist=straight_edges, ax=ax, 
                       edge_color='midnightblue', alpha=0.5, width=1.5)
for u, v, rad in arc_edges:
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax,
                           edge_color='midnightblue', alpha=0.5, width=1.5,
                           connectionstyle=f"arc3,rad={rad}",
                           arrows=True, arrowstyle="-")
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, 
                       edgecolors='black', node_size=1800, linewidths=1.5)
nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, 
                        font_size=16, font_weight='bold')
plt.margins(0.15)
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
plt.show()