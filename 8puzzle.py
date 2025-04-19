import heapq
import copy
import matplotlib.pyplot as plt
import numpy as np

def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()

def plot_all_matrices(solution, fgh_values):
    fig, axes = plt.subplots(1, len(solution), figsize=(4 * len(solution), 5))
    if len(solution) == 1:
        axes = [axes]

    for i, (matrix, (f, g, h), ax) in enumerate(zip(solution, fgh_values, axes)):
        ax.imshow(matrix, cmap='Blues')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Step {i}")
        for x in range(3):
            for y in range(3):
                if matrix[x][y] != 0:
                    ax.text(y, x, str(matrix[x][y]), ha='center', va='center', color='black', fontsize=14)
        ax.set_xlabel(f"f = {f}\ng = {g}, h = {h}", fontsize=12)

    plt.tight_layout()
    plt.show()

def is_goal(state, goal):
    return state == goal

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_possible_moves(blank_pos):
    x, y = blank_pos
    moves = []
    if x > 0: moves.append((x - 1, y))  # Move up
    if x < 2: moves.append((x + 1, y))  # Move down
    if y > 0: moves.append((x, y - 1))  # Move left
    if y < 2: moves.append((x, y + 1))  # Move right
    return moves

def make_move(state, blank_pos, new_blank_pos):
    x, y = blank_pos
    new_x, new_y = new_blank_pos
    new_state = copy.deepcopy(state)
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state

def calculate_h(state, goal):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                misplaced_tiles += 1
    return misplaced_tiles

def a_star_search(initial_state, goal_state):
    open_list = []
    closed_list = set()

    blank_pos = get_blank_position(initial_state)
    heapq.heappush(open_list, (0, 0, initial_state, blank_pos, [], []))  # (f(n), g(n), state, blank_pos, path, fgh_values)

    while open_list:
        f, g, current_state, blank_pos, path, fgh_values = heapq.heappop(open_list)

        # Print the step
        print("Current state (g =", g, ", h =", f - g, ", f =", f, "):")
        print_matrix(current_state)

        if is_goal(current_state, goal_state):
            print("Goal reached!")
            return path + [current_state], fgh_values + [(f, g, f - g)]

        closed_list.add(tuple(map(tuple, current_state)))

        for move in get_possible_moves(blank_pos):
            new_state = make_move(current_state, blank_pos, move)
            new_blank_pos = move

            if tuple(map(tuple, new_state)) in closed_list:
                continue

            h = calculate_h(new_state, goal_state)
            new_f = g + 1 + h
            heapq.heappush(open_list, (
                new_f, g + 1, new_state, new_blank_pos,
                path + [current_state],
                fgh_values + [(f, g, f - g)]
            ))

    print("No solution found!")
    return [], []

# Initial and goal states
initial_state = [[2, 8, 3],
                 [1, 6, 4],
                 [7, 0, 5]]

goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

# Perform A* search
solution, fgh_values = a_star_search(initial_state, goal_state)

# Plot the solution path
if solution:
    matrices = [np.array(step) for step in solution]
    plot_all_matrices(matrices, fgh_values)
