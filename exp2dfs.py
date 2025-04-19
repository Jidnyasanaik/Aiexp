import networkx as nx
import matplotlib.pyplot as plt

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

# DFS function for routing
def dfs_routing(graph, start, end, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == end:
        return path

    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs_routing(graph, neighbor, end, path.copy(), visited.copy())
            if result:
                return result

    return None

# Define source and destination
source = 'A'
destination = 'G'
path = dfs_routing(network, source, destination)

# Display the IP route in the terminal
if path:
    ip_route = [ip_map[node] for node in path]
    print("DFS Packet Route (IP Path):", " -> ".join(ip_route))
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

# Highlight DFS path
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightgreen')

plt.title("DFS Packet Routing with IPs", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
