import networkx as nx
import matplotlib.pyplot as plt
import math

# Initialize the graph
G = nx.Graph()

# Define edges exactly as traced from your drawing
edges = [
    # Perimeter hexagon
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1),
    # Inner cross connections
    (1, 3), (3, 5), (6, 4), (6, 2),
    # Connections to the center node (7)
    (7, 1), (7, 2), (7, 4), (7, 5)
]

G.add_edges_from(edges)

# Define explicit (x, y) positions to match the visual layout
# Node 7 is at the origin (0,0), and 1-6 form a hexagon
pos = {
    1: (-0.5, math.sqrt(3)/2),  # Top-Left
    2: (0.5, math.sqrt(3)/2),   # Top-Right
    3: (1.0, 0),                # Right
    4: (0.5, -math.sqrt(3)/2),  # Bottom-Right
    5: (-0.5, -math.sqrt(3)/2), # Bottom-Left
    6: (-1.0, 0),               # Left
    7: (0.0, 0)                 # Center
}

# Set up the plot
plt.figure(figsize=(8, 8))

# Draw the graph with styling to match your sketch
nx.draw(
    G, pos, 
    with_labels=True, 
    node_color='maroon',     # Dark red like your sketch
    font_color='white',      # White text for contrast
    font_size=16,
    font_weight='bold', 
    node_size=1200, 
    edge_color='black', 
    width=2.5                # Thicker lines
)

# Add a title and adjust margins so nodes aren't cut off
plt.title("Graph G4 Reproduction", fontsize=18, fontweight='bold', pad=20)
plt.margins(0.15) 

# Display the graph
plt.show()