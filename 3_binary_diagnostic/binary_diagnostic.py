import numpy as np
from typing import Tuple, List


def str_to_matrix(data: List[str]) -> np.ndarray:
    total_row = len(data)
    if total_row == 0:
        return np.array([])
    total_col = len(data[0]) - 1
    return np.array([[int(row[col]) for col in range(total_col)] for row in data])

def binary_diagnostic(data_matrix: np.ndarray) -> Tuple[int, int]:
    total_row = len(data_matrix)
    if total_row == 0:
        return 0, 0

    half_row = total_row // 2
    integration = np.sum(data_matrix, axis=0)
    gamma = 0
    epsilon = 0
    for item in integration:
        bits = 1 if item > half_row else 0
        gamma *= 2
        gamma += bits
        epsilon *= 2
        epsilon -= (bits - 1)
    return gamma, epsilon

def bit_criteria_oxygen(data_matrix: np.ndarray) -> int:
    total_row = len(data_matrix)
    if total_row == 0:
        return 0

    for i in range(len(data_matrix[0])):
        num_ones = np.count_nonzero(data_matrix[:, i] == 1)
        num_rows = data_matrix.shape[0]
        if num_ones > num_rows // 2 or (num_rows % 2 == 0 and num_ones == num_rows // 2):
            data_matrix = data_matrix[data_matrix[:, i] == 1]
        else:
            data_matrix = data_matrix[data_matrix[:, i] == 0]
        if len(data_matrix) == 1:
            res = 0
            for item in data_matrix[0]:
                res *= 2
                res += item
            return res
    return -1
    
def bit_criteria_co2(data_matrix: np.ndarray) -> int:
    total_row = len(data_matrix)
    if total_row == 0:
        return 0

    for i in range(len(data_matrix[0])):
        num_ones = np.count_nonzero(data_matrix[:, i] == 1)
        num_rows = data_matrix.shape[0]
        if num_ones > num_rows // 2 or (num_rows % 2 == 0 and num_ones == num_rows // 2):
            data_matrix = data_matrix[data_matrix[:, i] == 0]
        else:
            data_matrix = data_matrix[data_matrix[:, i] == 1]
        if len(data_matrix) == 1:
            res = 0
            for item in data_matrix[0]:
                res *= 2
                res += item
            return res

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        data = f.readlines()
        data_matrix = str_to_matrix(data)

        gamma, epsilon = binary_diagnostic(data_matrix)
        print(gamma*epsilon)

        oxygen_gen_rating = bit_criteria_oxygen(data_matrix)
        co2_gen_rating = bit_criteria_co2(data_matrix)
        print(oxygen_gen_rating * co2_gen_rating)

