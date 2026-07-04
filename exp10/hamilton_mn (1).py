import matplotlib.pyplot as plt
import networkx as nx
def create_graph():
    G = nx.Graph()
    edges = [
        ("V1", "V2"),
        ("V1", "V3"),
        ("V2", "V4"),
        ("V3", "V4"),
        ("V4", "V5"),
        ("V4", "V6"),
        ("V5", "V6"),
        ("V2", "V5")    ]
    G.add_edges_from(edges)
    pos = {
        "V1": (0, 2),
        "V2": (-1.5, 1),
        "V3": (1.5, 1),
        "V4": (0, 0),
        "V5": (-1.5, -1.5),
        "V6": (1.5, -1.5)    }
    return {
        "name": "Hamiltonian Graph",
        "G": G,
        "pos": pos    }
def find_hamiltonian_cycle(G):
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return None
    start_node = nodes[0]
    path = [start_node]
    def backtrack(curr):
        if len(path) == n:
            if G.has_edge(path[-1], start_node):
                return path + [start_node]
            return None
        for neighbor in G.neighbors(curr):
            if neighbor not in path:
                path.append(neighbor)
                result = backtrack(neighbor)
                if result:
                    return result
                path.pop()
        return None
    return backtrack(start_node)
def draw_cycle(G, pos, cycle, name):
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color='lightblue',
        edge_color='gray',
        node_size=1200,
        font_weight='bold',
        width=2    )
    if cycle:
        edges = [
            (cycle[i], cycle[i+1])
            for i in range(len(cycle)-1)        ]
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color='red',
            width=4        )
        plt.title(
            f"{name}: Hamiltonian Cycle Found\n{cycle}",
            fontsize=13,
            fontweight='bold'        )
    else:
        plt.title(
            f"{name}: No Hamiltonian Cycle Found",
            fontsize=13,
            fontweight='bold'        )
    plt.axis('off')
    plt.show()
def main():
    config = create_graph()
    G = config["G"]
    pos = config["pos"]
    name = config["name"]
    print(f"Finding Hamiltonian Cycle for {name}...")
    cycle = find_hamiltonian_cycle(G)
    if cycle:
        print(f"Found Cycle: {cycle}")
    else:
        print("No Hamiltonian Cycle exists.")
    draw_cycle(G, pos, cycle, name)
if __name__ == "__main__":
    main()