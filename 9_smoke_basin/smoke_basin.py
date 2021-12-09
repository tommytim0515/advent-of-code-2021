import math
from typing import List


def get_inputs(file_name: str) -> List[List[int]]:
    with open(file_name) as f:
        data = f.readlines()
    return [[int(c) for c in line.strip()] for line in data]


def sum_risk_level_of_low_points(map_data: List[List[int]]) -> int:
    sum_risk_level = 0
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if i - 1 >= 0 and map_data[i - 1][j] <= map_data[i][j]:
                continue
            if i + 1 < len(map_data) and map_data[i + 1][j] <= map_data[i][j]:
                continue
            if j - 1 >= 0 and map_data[i][j - 1] <= map_data[i][j]:
                continue
            if j + 1 < len(map_data[i]) and map_data[i][j + 1] <= map_data[i][j]:
                continue
            sum_risk_level += (map_data[i][j] + 1)
    return sum_risk_level


def init_map_data(map_data: List[List[int]]) -> None:
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == 9:
                map_data[i][j] = 1
            else:
                map_data[i][j] = 0


def tag_basin(map_data: List[List[int]], i: int, j: int) -> int:
    if map_data[i][j] != 0:
        return 0
    map_data[i][j] = 1
    res = 1
    if i - 1 >= 0:
        res += tag_basin(map_data, i - 1, j)
    if i + 1 < len(map_data):
        res += tag_basin(map_data, i + 1, j)
    if j - 1 >= 0:
        res += tag_basin(map_data, i, j - 1)
    if j + 1 < len(map_data[i]):
        res += tag_basin(map_data, i, j + 1)
    return res


def multiplication_of_three_largest_basins(map_data: List[List[int]]) -> int:
    init_map_data(map_data)
    top_three: List[int] = []
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] != 0:
                continue
            size_basin = tag_basin(map_data, i, j)
            if len(top_three) < 3:
                top_three.append(size_basin)
            else:
                top_three = sorted(top_three)
                if size_basin > top_three[0]:
                    top_three[0] = size_basin
    return math.prod(top_three)


if __name__ == '__main__':
    map_data = get_inputs('input.txt')
    print(f'Sum of risk level: {sum_risk_level_of_low_points(map_data)}')
    print('Multiplication of the sizes of top 3 basins: {}'
          .format(multiplication_of_three_largest_basins(map_data)))
