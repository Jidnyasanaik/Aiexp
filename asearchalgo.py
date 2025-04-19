import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Define the graph with nodes and edges (neighbor, cost)
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1), ('E', 3)],
    'D': [('B', 5), ('C', 1), ('E', 2)],
    'E': [('C', 3), ('D', 2)]
}

# Define heuristic values (h) for each node
heuristic = {
    'A': 7,
    'B': 6,
    'C': 2,
    'D': 1,
    'E': 0
}

# A* search algorithm
def a_star_search(start, goal, graph, heuristic):
    open_list = []
    closed_list = set()
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic[start]}
    
    heapq.heappush(open_list, (f_score[start], start))
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score  # Return path and g_scores
        
        closed_list.add(current)
        
        for neighbor, cost in graph[current]:
            if neighbor in closed_list:
                continue
            
            tentative_g_score = g_score[current] + cost
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, g_score

# Run the A* search
start_node = 'A'
goal_node = 'E'
path, g_scores = a_star_search(start_node, goal_node, graph, heuristic)

# Print the path
print(f"Path from {start_node} to {goal_node}: {path}")

# Create a graph for plotting
G = nx.Graph()
for node in graph:
    for neighbor, cost in graph[node]:
        G.add_edge(node, neighbor, weight=cost)

# Plotting the graph
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 7))

# Draw the base graph
nx.draw(G, pos, with_labels=True, node_size=600, node_color='skyblue', font_size=16, font_weight='bold', edge_color='gray')

# Show heuristic values on nodes
for node in G.nodes():
    x, y = pos[node]
    plt.text(x, y + 0.1, f"h={heuristic[node]}", fontsize=10, ha='center', color='blue')

# Highlight the path found by A* search
if path:
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)
    
    # Show f(n) = g(n) + h(n) on nodes in the path
    for node in path:
        f = g_scores[node] + heuristic[node]
        x, y = pos[node]
        plt.text(x, y - 0.15, f"f={g_scores[node]}+{heuristic[node]}={f}", fontsize=9, ha='center', color='darkred')

plt.title(f"A* Search Path from {start_node} to {goal_node}")
plt.axis('off')
plt.show()
