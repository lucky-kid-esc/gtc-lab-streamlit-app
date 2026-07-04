import matplotlib.pyplot as plt 
import networkx as nx 
import math
def create_graphs():
    G4 = nx.Graph()
    edges4 = [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), 
        (1, 3), (3, 5), (6, 4), (6, 2),                 
        (7, 1), (7, 2), (7, 4), (7, 5)                  
    ]
    G4.add_edges_from(edges4)   
    pos4 = {
        1: (-0.5, math.sqrt(3)/2),  
        2: (0.5, math.sqrt(3)/2),   
        3: (1.0, 0),                
        4: (0.5, -math.sqrt(3)/2),  
        5: (-0.5, -math.sqrt(3)/2), 
        6: (-1.0, 0),               
        7: (0.0, 0)                     }
    G5 = nx.Graph()
    nodes5 = [1, 2, 3, 4, 5, 6, 7]
    edges5 = [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1),             
        (1, 4), (2, 5), (3, 6), (4, 7), (5, 1), (6, 2), (7, 3)                  ]
    G5.add_nodes_from(nodes5)
    G5.add_edges_from(edges5)   
    pos5 = {}
    for i, node in enumerate(nodes5):
        theta = math.pi / 2 - i * (2 * math.pi / 7)
        pos5[node] = (math.cos(theta), math.sin(theta))        
    return G4, pos4, G5, pos5
def get_cycle_girth(G):
    cycles = nx.cycle_basis(G)
    if not cycles:
        return 0
    return min(len(cycle) for cycle in cycles)
def print_graph_stats(G, name):
    vertices = G.number_of_nodes()
    edges = G.number_of_edges()
    degree_sequence = sorted([d for n, d in G.degree()])
    girth = get_cycle_girth(G)
    print(f"Graph {name}")
    print(f"Vertices         : {vertices}")
    print(f"Edges            : {edges}")
    print(f"Degree Sequence  : {degree_sequence}")
    print(f"Cycle Girth      : {girth}\n")
def deg_seq(G):
    ds = sorted([d for _, d in nx.degree(G)], reverse=True)
    return ds
def get_adj_list(G):
    vertices = list(G.nodes())
    edges = list(G.edges())
    adj = {v: [] for v in vertices}
    for e0,e1 in edges:
        adj[e0].append(e1)
        adj[e1].append(e0)
    return adj
def cycles(G):
    vertices = list(G.nodes())
    edges = list(G.edges())
    adj_list = get_adj_list(G)
    cycles_path = set()
    def dfs(cur, parent, path):
        if cur == root and len(path)>=3:
            norm_cyl = tuple(sorted(path))
            cycles_path.add(norm_cyl)
            return  
        for v in adj_list[cur]:
            if v == parent:
                continue
            if v < root:
                continue
            if vis[v] == True and v!=root:
                continue            
            if v != root:
                vis[v] = True
            dfs(v, cur, path + [v])
            if v != root:
                vis[v] = False
    for root in vertices:
        vis = {v: False for v in vertices}
        vis[root] = True
        dfs(root, -1, [root])
    return cycles_path
def cyl_degree(G, cycles):
    cyl_deg = []
    for cyl in cycles:
        node = sorted([G.degree(n) for n in cyl])
        cyl_deg.append(node)
    return sorted(cyl_deg)
def bi_map(g1, g2):
    def solve(mapping, unmapped1, unmapped2):
        if not unmapped1:
            return mapping
        u = unmapped1[0]        
        for v in unmapped2:
            if g1.degree(u) == g2.degree(v):
                is_consistent = True
                for u_mapped, v_mapped in mapping.items():
                    if g1.has_edge(u, u_mapped) != g2.has_edge(v, v_mapped):
                        is_consistent = False
                        break                
                if is_consistent:
                    new_mapping = mapping.copy()
                    new_mapping[u] = v
                    solution = solve(new_mapping, unmapped1[1:], [n for n in unmapped2 if n != v])
                    if solution:
                        return solution
        return None
    nodes1 = sorted(list(g1.nodes()), key=g1.degree, reverse=True)
    nodes2 = list(g2.nodes())
    return solve(mapping={}, unmapped1=nodes1, unmapped2=nodes2)
def is_iso(g1, g2):
    v1 = nx.number_of_nodes(g1)
    v2 = nx.number_of_nodes(g2)
    if(v1 != v2):
        print("Not isomorphic (Vertex mismatch)")
        return 
    e1 = nx.number_of_edges(g1)
    e2 = nx.number_of_edges(g2)
    if(e1 != e2):
        print("Not isomorphic (Edges mismatch)")
        return
    d1 = deg_seq(g1)
    d2 = deg_seq(g2)
    if(d1 != d2):
        print("Not isomorphic (Degree Sequence mismatch)")
        return     
    cyl1 = cycles(g1)
    cyl2 = cycles(g2)
    if(len(cyl1) != len(cyl2)):
        print("Not isomorphic (Cycle Count mismatch)")
        return 
    cyl_deg1 = cyl_degree(g1, cyl1)
    cyl_deg2 = cyl_degree(g2, cyl2)
    if(cyl_deg1 != cyl_deg2):
        print("Not isomorphic (Cycle degree mismatch)")
        return
    mapping = bi_map(g1, g2)
    if not mapping:
        print("Graphs are not isomorphic (bijection not found).")
        return
    print("Graphs are Isomorphic")
    print(f"|v1| = {v1}     |v2| = {v2}")
    print(f"|e1| = {e1}     |e2| = {e2}")
    print(f"deg1 = {d1}     d2 = {d2}")
    print(f"Mapping: {mapping}")
def plot_graph(g, pos, ax_idx, title, ax):
    nx.draw(
        g, pos=pos, ax=ax[ax_idx], with_labels=True, node_color='maroon',
        font_color='white', font_size=16, font_weight='bold', 
        node_size=1200, edge_color='black', width=2.5
    )
    ax[ax_idx].set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax[ax_idx].margins(0.15) 
def main():
    G4, pos4, G5, pos5 = create_graphs()

    print_graph_stats(G4, "G4")
    print_graph_stats(G5, "G5")
    print("Isomorphism Check (Manual Custom Function):")
    is_iso(G4, G5)
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    plot_graph(G4, pos4, 0, "Graph G4", ax)
    plot_graph(G5, pos5, 1, "Graph G5", ax)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()