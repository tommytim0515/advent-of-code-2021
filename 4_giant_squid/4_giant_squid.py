import numpy as np
from typing import List, Tuple

MATRIX_SIZE = 5
NUM_LINE_SEGMENT = 6


def get_inputs(filename: str) -> Tuple[List[int], np.ndarray]:
    with open(filename, 'r') as f:
        data = f.read().splitlines()
        sequence = [int(x) for x in data[0].split(',')]
        matrices = np.array([[[int(x) for x in data[i+j].split()] for j in range(
            NUM_LINE_SEGMENT - 1)] for i in range(2, len(data), NUM_LINE_SEGMENT)])
        return sequence, matrices


def bingo_subsystem_win_first(seq: List[int], matrices: np.ndarray) -> int:
    for num in seq:
        for i in range(len(matrices)):
            coors = np.argwhere(matrices[i] == num)
            for coor in coors:
                matrices[i][coor[0], coor[1]] = -1
                if np.sum(matrices[i][coor[0]]) == -5 or np.sum(matrices[i][:, coor[1]]) == -5:
                    return num * np.sum(matrices[i][matrices[i] != -1])
    return 0


def bingo_subsystem_win_last(seq: List[int], matrices: np.ndarray) -> int:
    wins = set()
    res = 0
    for num in seq:
        for i in range(len(matrices)):
            coors = np.argwhere(matrices[i] == num)
            for coor in coors:
                matrices[i][coor[0], coor[1]] = -1
                if np.sum(matrices[i][coor[0]]) == -5 or np.sum(matrices[i][:, coor[1]]) == -5:
                    if i not in wins:
                        wins.add(i)
                        res = num * np.sum(matrices[i][matrices[i] != -1])
    return res


if __name__ == '__main__':
    seq, matrices = get_inputs('input.txt')
    print('Win first: {}'.format(bingo_subsystem_win_first(seq, matrices)))
    print('Win last: {}'.format(bingo_subsystem_win_last(seq, matrices)))
