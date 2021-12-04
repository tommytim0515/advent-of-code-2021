import numpy as np
from typing import List, Tuple
from collections import OrderedDict

def get_inputs(filename: str) -> Tuple[List[int], List[np.ndarray]]:
    with open(filename, 'r') as f:
        data = f.read().splitlines()
        sequence = [int(x) for x in data[0].split(',')]
        matrices = []
        for i in range(2, len(data), 6):
            arr = np.matrix([
                [int(x) for x in data[i].split()],
                [int(x) for x in data[i+1].split()],
                [int(x) for x in data[i+2].split()],
                [int(x) for x in data[i+3].split()],
                [int(x) for x in data[i+4].split()]
            ])
            matrices.append(arr)
        return sequence, matrices

def unmarked_sum(matrix: np.ndarray, mask: np.ndarray) -> int:
    unmarked_coors = np.argwhere(mask == 0)
    unmarked_sum = 0
    for unmarked_coor in unmarked_coors:
        unmarked_sum += matrix[unmarked_coor[0], unmarked_coor[1]]
    return unmarked_sum

def bingo_subsystem_win_first(seq: List[int], matrices: List[np.ndarray]) -> int:
    masks = [np.zeros((5, 5), dtype=int) for _ in range(len(matrices))]
    for num in seq:
        for i in range(len(matrices)):
            coors = np.argwhere(matrices[i] == num)
            for coor in coors:
                masks[i][coor[0], coor[1]] = 1
                if np.sum(masks[i][coor[0]]) == 5 or np.sum(masks[i].T[coor[1]]) == 5:
                    return num * unmarked_sum(matrices[i], masks[i])
    return 0

def bingo_subsystem_win_last(seq: List[int], matrices: List[np.ndarray]) -> int:
    masks = [np.zeros((5, 5), dtype=int) for _ in range(len(matrices))]
    win_dict = {}
    for num in seq:
        for i in range(len(matrices)):
            coors = np.argwhere(matrices[i] == num)
            for coor in coors:
                masks[i][coor[0], coor[1]] = 1
                if np.sum(masks[i][coor[0]]) == 5 or np.sum(masks[i].T[coor[1]]) == 5:
                    if i not in win_dict:
                        win_dict[i] = num * unmarked_sum(matrices[i], masks[i])
    if len(win_dict) == 0:
        return 0
    idx = next(reversed(win_dict))
    return win_dict[idx]


if __name__ == '__main__':
    seq, matrices = get_inputs('input.txt')
    print(bingo_subsystem_win_first(seq, matrices))
    print(bingo_subsystem_win_last(seq, matrices))
