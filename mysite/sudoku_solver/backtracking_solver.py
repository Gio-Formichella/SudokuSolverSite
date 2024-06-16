import copy
import random
from queue import Queue

import numpy as np

from .cell import Cell


async def backtracking_solver(puzzle, var_strategy="static", inference_strategy="mac", consumer=None) \
        -> (np.ndarray or None, int, int):
    """
    :param puzzle: Sudoku puzzle matrix
    :param var_strategy: Strategy for unassigned variable selection:
        - "static": First variable in static order
        - "random": Randomly selected
        - "mrv": Minimum-remaining-values heuristic
    :param inference_strategy: Type of domain reduction inference:
        - "mac": Maintaining arc consistency
        - "forward_checking": Forward checking, only neighbouring variables are checked
    :param consumer: reference to BoardConsumer, used to send assignment updates
    :return:  Matrix solution or None if puzzle has no solution, number of assignments and number of backtracks
    """
    board = np.empty((9, 9), dtype=Cell)

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] is not None:
                board[i, j] = Cell(puzzle[i][j])
            else:
                board[i, j] = Cell()

    # Initializing assignments and backtracks counters
    counters = [0, 0]  # [assignments counter, backtracks counter

    if not ac3(board, counters):
        return None, counters[0], counters[1]
    result = await backtracking_search(board, var_strategy, inference_strategy, counters, consumer)

    if result is not None:
        for i in range(9):
            for j in range(9):
                result[i][j] = result[i][j].value

    return result, counters[0], counters[1]


def ac3(board, counters) -> bool:
    queue = Queue()
    # Arcs relative to row and column constraints
    for i in range(9):
        for j in range(9):
            for k in range(j + 1, 9):
                # First two indices are the position of the first variable in the matrix while the last two are for
                # the second variable
                queue.put((i, j, i, k))
                queue.put((i, k, i, j))
            for m in range(i + 1, 9):
                queue.put((i, j, m, j))
                queue.put((m, j, i, j))
    # Arcs relative to square constraints
    for sr in range(3):  # Square rows
        for sc in range(3):  # Square columns
            for i in range(sr * 3, sr * 3 + 3):  # Row index within the square
                for j in range(sc * 3, sc * 3 + 3):  # Column index within the square
                    for k in range(i + 1, sr * 3 + 3):
                        for m in range(j + 1, sc * 3 + 3):
                            queue.put((i, j, k, m))
                            queue.put((k, m, i, j))
                        for n in range(sc * 3, j):
                            queue.put((i, j, k, n))
                            queue.put((k, n, i, j))

    return propagate_constraints(board, queue, counters)


def propagate_constraints(board, queue, counters) -> bool:
    """
    :param board: Sudoku puzzle board
    :param queue: Queue of constraints to be checked
    :param counters: List of counters for assignments and backtracks
    :return: True if all constraints are satisfiable, False otherwise
    """

    while not queue.empty():
        t = queue.get()
        i1, j1, i2, j2 = t[0], t[1], t[2], t[3]
        if revise(board, i1, j1, i2, j2):
            d_length = len(board[i1, j1].domain)  # Number of values still in domain
            if d_length == 0:
                # Problem has no solution
                return False
            if d_length == 1:
                board[i1, j1].set_value(board[i1, j1].domain[0])  # Assigning value if only one is available
                counters[0] += 1
            # Propagation to all neighbors
            for k in range(9):
                if k != j1 and (i1, k) != (i2, j2):
                    queue.put((i1, k, i1, j1))
                if k != i1 and (k, j1) != (i2, j2):
                    queue.put((k, j1, i1, j1))
            sr = i1 // 3
            sc = j1 // 3
            for i in range(sr * 3, sr * 3 + 3):
                for j in range(sc * 3, sc * 3 + 3):
                    if (i, j) not in ((i1, j1), (i2, j2)):
                        queue.put((i, j, i1, j1))

    return True


def revise(board, i1: int, j1: int, i2: int, j2: int) -> bool:
    revised = False
    for x in board[i1, j1].domain:
        found = False  # x admissibility
        for y in board[i2, j2].domain:
            if y != x:
                found = True

        if not found:
            board[i1, j1].domain.remove(x)
            revised = True

    return revised


async def backtracking_search(board, var_strategy: str, inference_strategy: str, counters: list, consumer) \
        -> np.ndarray or None:
    return await backtrack(board, var_strategy, inference_strategy, counters, consumer)


async def backtrack(board, var_strategy: str, inference_strategy: str, counters: list, consumer) -> np.ndarray or None:
    # Checking for complete assignment
    found = False
    for i in range(9):
        for j in range(9):
            if board[i, j].value is None:
                found = True
    if not found:
        return board

    var = select_unassigned_variable(board, var_strategy)  # tuple (row, column)
    for value in order_domain_values(board, var):
        inference_board = inference(copy.deepcopy(board), var, value, inference_strategy, counters)
        counters[0] += 1  # Assignment
        if consumer is not None:
            await consumer.send_assignment_update(var[0], var[1], value, counters[0], counters[1])
        if inference_board is not None:
            result = await backtrack(inference_board, var_strategy, inference_strategy, counters, consumer)
            if result is not None:
                return result

        counters[1] += 1  # Backtracking

    return None


def select_unassigned_variable(board, strategy) -> tuple or None:
    unassigned_var = []
    for i in range(9):
        for j in range(9):
            if board[i, j].value is None:
                unassigned_var.append((i, j))
    if len(unassigned_var) > 0:
        match strategy:
            case "static":  # Choosing first variable in static ordering
                return unassigned_var[0]
            case "random":  # Randomly selecting unassigned variable
                idx = random.randint(0, len(unassigned_var) - 1)
                return unassigned_var[idx]
            case "mrv":
                mrvv = unassigned_var[0]  # Mrv variable
                mrv = len(board[mrvv[0], mrvv[1]].domain)
                for var in unassigned_var:
                    if len(board[var[0], var[1]].domain) < mrv:
                        mrvv = var
                        mrv = len(board[var[0], var[1]].domain)
                return mrvv
    return None


def order_domain_values(board: np.ndarray[Cell], var: tuple) -> list:
    """
    :param board: Sudoku puzzle board
    :param var: indices of selected variable
    :return: list of domain values in least-constraining order
    """

    i = var[0]
    j = var[1]
    least_constraining_value = []  # Will store for every value in variable domain (value, constraint_score)
    neighbors = []  # Stores neighbouring variables
    # Adding neighbors
    for k in range(9):
        if k != j:
            neighbors.append((i, k))
        if k != i:
            neighbors.append((k, j))
    sr = i // 3  # Square row of variable
    sc = j // 3  # Square column of variable
    for m in range(sr * 3, sr * 3 + 3):
        for n in range(sc * 3, sc * 3 + 3):
            if m != i and n != j:
                neighbors.append((m, n))

    for value in board[i, j].domain:
        count = 0  # Times value is present in neighbors' domain
        for n in neighbors:
            if value in board[n[0], n[1]].domain:
                count += 1
        least_constraining_value.append((value, count))

    least_constraining_value.sort(key=lambda x: x[1])
    return [t[0] for t in least_constraining_value]


def inference(board, var, value, inference_strategy, counters) -> np.ndarray or None:
    i = var[0]
    j = var[1]
    board[i, j].set_value(value)
    match inference_strategy:
        case "mac":
            if mac(board, (i, j), counters) is not None:
                return board
            else:
                return None
        case "forward_checking":
            if forward_checking(board, (i, j), counters) is not None:
                return board
            else:
                return None


def mac(board, var, counters) -> np.ndarray or None:
    i = var[0]
    j = var[1]
    queue = Queue()
    for k in range(9):
        if k != j and board[i, k].value is None:
            queue.put((i, k, i, j))
        if k != i and board[k, j].value is None:
            queue.put((k, j, i, j))
    sr = i // 3  # Square row of variable
    sc = j // 3  # Square column of variable
    for m in range(sr * 3, sr * 3 + 3):
        for n in range(sc * 3, sc * 3 + 3):
            if (m, n) != (i, j) and board[m, n].value is None:
                queue.put((m, n, i, j))

    if propagate_constraints(board, queue, counters):
        return board
    return None


def forward_checking(board, var, counters) -> np.ndarray or None:
    i = var[0]
    j = var[1]
    queue = Queue()

    for k in range(9):
        if k != j and board[i, k].value is None:
            queue.put((i, k, i, j))
        if k != i and board[k, j].value is None:
            queue.put((k, j, i, j))
    sr = i // 3  # Square row of variable
    sc = j // 3  # Square column of variable
    for m in range(sr * 3, sr * 3 + 3):
        for n in range(sc * 3, sc * 3 + 3):
            if (m, n) != (i, j) and board[m, n].value is None:
                queue.put((m, n, i, j))
    while not queue.empty():
        t = queue.get()
        i1, j1, i2, j2 = t[0], t[1], t[2], t[3]
        if revise(board, i1, j1, i2, j2):
            d_length = len(board[i1, j1].domain)
            if d_length == 0:
                # Problem has no solution
                return None
            if d_length == 1:
                board[i1, j1].set_value(board[i1, j1].domain[0])
                counters[0] += 1

    return board
