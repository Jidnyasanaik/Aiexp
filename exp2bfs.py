import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Define the simple branching network
network = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'E', 'F'],
    'D': ['B'],
    'E': ['C'],
    'F': ['C', 'G'],
    'G': ['F']
}

# IP addresses for each node
ip_map = {
    'A': '10.0.0.1',
    'B': '10.0.0.2',
    'C': '10.0.0.3',
    'D': '10.0.0.4',
    'E': '10.0.0.5',
    'F': '10.0.0.6',
    'G': '10.0.0.7'
}

# BFS function for routing
def bfs_routing(graph, start, end):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = path + [neighbor]
                queue.append(new_path)

    return None

# Define source and destination
source = 'A'
destination = 'G'
path = bfs_routing(network, source, destination)

# Display the IP route in the terminal
if path:
    ip_route = [ip_map[node] for node in path]
    print("BFS Packet Route (IP Path):", " -> ".join(ip_route))
else:
    print("No route found")

# Create the graph
G = nx.DiGraph()
for node, neighbors in network.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Custom positions for tree-like layout
pos = {
    'A': (0, 3),
    'B': (-1.5, 2),
    'C': (1.5, 2),
    'D': (-2, 1),
    'E': (1, 1),
    'F': (2, 1),
    'G': (2.5, 0)
}

# Labels with IPs
ip_labels = {node: f"{node}\n{ip_map[node]}" for node in G.nodes()}

# Plotting
plt.figure(figsize=(10, 6))
nx.draw(G, pos, labels=ip_labels, with_labels=True,
        node_color='skyblue', node_size=1600, font_size=9,
        font_weight='bold', edge_color='gray', arrows=False)

# Highlight BFS path
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=3)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightyellow')

plt.title("BFS Packet Routing with IPs", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
