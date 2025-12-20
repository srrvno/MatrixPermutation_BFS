import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import random as rd
import time


# Conversion between flat tuple (state) and 3x3 matrix
def ttom(state):
    return np.array(state).reshape(3, 3)


def mtot(matrix):
    return tuple(np.array(matrix).flatten())


# Clockwise rotation of a 2x2 submatrix (indices 0-3)
def giro(num, matrix):
    m = np.array(matrix).copy()
    position_matrix = [
        [(0, 0), (0, 1), (1, 1), (1, 0)],  # top-left
        [(0, 1), (0, 2), (1, 2), (1, 1)],  # top-right
        [(1, 0), (1, 1), (2, 1), (2, 0)],  # bottom-left
        [(1, 1), (1, 2), (2, 2), (2, 1)],  # bottom-right
    ]
    positions = position_matrix[num]
    values = deque([m[i] for i in positions])
    values.rotate(1)
    for idx, pos in enumerate(positions):
        m[pos] = values[idx]
    return m


# Wrapper to work on states (tuples)
def giro_w(num, state):
    matrix = ttom(state)
    rotated = giro(num, matrix)
    return mtot(rotated)


# Successor generation (resulting state and operator used)
def gen_suc_matrix(state):
    return [(giro_w(i, state), i) for i in range(4)]


# Reconstruct rotation sequence from the parent dictionary
def backtrack(gen_tree, init_state, goal):
    opps = deque()
    elem = goal
    while elem != init_state:
        parent, op = gen_tree[elem]
        opps.appendleft(op)
        elem = parent
    return opps


# BFS that returns the minimal rotation sequence (if it exists)
def matrix_BFS(init_state, goal):
    if init_state == goal:
        return deque()

    cola = deque([init_state])
    on_cola = {init_state}
    explored = set()
    gen_tree = {}

    while cola:
        elem = cola.popleft()
        explored.add(elem)

        for succ, op in gen_suc_matrix(elem):
            if succ in explored or succ in on_cola:
                continue
            gen_tree[succ] = (elem, op)
            if succ == goal:
                return backtrack(gen_tree, init_state, goal)
            cola.append(succ)
            on_cola.add(succ)

    return None


# Apply a rotation sequence to validate solutions
def rep_ops(state, op_sec):
    for op in op_sec:
        state = giro_w(op, state)
    return state


def check_ops_sec(state, op_sec, goal):
    return rep_ops(state, op_sec) == goal


# Performance measurement following the notebook logic
def test_performance():
    print("--- Execution Time Table (BFS) ---")
    state1 = mtot(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    test_scenarios = [
        ("Easy", 3),
        ("Medium", 8),
        ("Hard", 15),
    ]

    results = []
    for name, num_rotations in test_scenarios:
        print(f"\nRunning scenario: {name} (Rotations applied: {num_rotations})...")

        goal = state1
        for _ in range(num_rotations):
            goal = giro_w(rd.randint(0, 3), goal)

        start_time = time.time()
        ops_sec = matrix_BFS(state1, goal)
        end_time = time.time()

        time_taken = end_time - start_time
        length = len(ops_sec) if ops_sec is not None else None

        results.append(
            {
                "Scenario": name,
                "Rotations Generated": num_rotations,
                "BFS Sequence Length": length,
                "Time": time_taken,
            }
        )

    print("\n" + "=" * 69)
    print("| Scenario | Rotations Generated | BFS Sequence Length | Time (s) |")
    print("|-----------|-----------------|------------------------|------------|")
    for res in results:
        length_str = res["BFS Sequence Length"] if res["BFS Sequence Length"] is not None else "N/A"
        print(
            f"| {res['Scenario']:<9} | {res['Rotations Generated']:<19} | {length_str:<22} | {res['Time']:<10.4f} |"
        )
    print("=" * 69)

    scenarios = [res["Rotations Generated"] for res in results]
    times = [res["Time"] for res in results]

    plt.figure(figsize=(10, 5))
    plt.plot(scenarios, times, marker="o")
    plt.xlabel("Rotations")
    plt.ylabel("Execution time (s)")
    plt.title("BFS performance by difficulty")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


if __name__ == "__main__":
    test_performance()
