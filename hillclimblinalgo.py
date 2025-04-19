class TowerOfHanoiState:
    def __init__(self, pegs):
        self.pegs = pegs

    def __str__(self):
        return f"Pegs: {self.pegs}"

    def get_heuristic(self):
        goal_state = [['d', 'c', 'b', 'a'], [], []]
        heuristic = 0
        for i in range(3):
            peg = self.pegs[i]
            goal_peg = goal_state[i]
            for j in range(min(len(peg), len(goal_peg))):
                if peg[j] == goal_peg[j]:
                    heuristic += 1
                else:
                    heuristic -= 1
        return heuristic

    def generate_successors(self):
        successors = []
        for i in range(3):
            if len(self.pegs[i]) > 0:
                disk = self.pegs[i][-1]
                for j in range(3):
                    if i != j and (len(self.pegs[j]) == 0 or self.pegs[j][-1] > disk):
                        new_pegs = [list(peg) for peg in self.pegs]
                        new_pegs[i].pop()
                        new_pegs[j].append(disk)
                        successors.append(TowerOfHanoiState(new_pegs))
        return successors

def hill_climbing(initial_state):
    current_state = initial_state
    print("Initial State:")
    print(current_state)
    print(f"Heuristic: {current_state.get_heuristic()}")

    goal_state = [['d', 'c', 'b', 'a'], [], []]
    print("\nGoal State:")
    print(f"Pegs: {goal_state}")
    print(f"Heuristic: {4}")

    while True:
        successors = current_state.generate_successors()
        if not successors:
            break

        next_state = max(successors, key=lambda state: state.get_heuristic())

        print(f"\nMove to next state:")
        print(next_state)
        print(f"Heuristic: {next_state.get_heuristic()}")

        if next_state.get_heuristic() <= current_state.get_heuristic():
            break

        current_state = next_state

    return current_state

# Initial state with pegs
initial_pegs = [['a', 'd', 'c', 'b'], [], []]
initial_state = TowerOfHanoiState(initial_pegs)

# Run Hill Climbing
goal_state = hill_climbing(initial_state)

print("\nGoal State Reached:")
print(goal_state)
print(f"Heuristic: {goal_state.get_heuristic()}")
