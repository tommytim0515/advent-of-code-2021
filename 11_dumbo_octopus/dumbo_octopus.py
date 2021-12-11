from typing import List


def get_inputs(file_name: str) -> List[List[int]]:
    with open(file_name, 'r') as f:
        data = f.readlines()
    return [[int(c) for c in line.strip()] for line in data]


def oct_flash_neighbor(oct_map: List[List[int]], i: int, j: int) -> int:
    num_flashes = 0
    for a in range(i-1, i+2):
        for b in range(j-1, j+2):
            if a == i and b == j:
                continue
            if a < 0 or b < 0 or a >= len(oct_map) or b >= len(oct_map[a]):
                continue
            if oct_map[a][b] == -1:
                continue
            oct_map[a][b] += 1
            if oct_map[a][b] > 9:
                oct_map[a][b] = -1
                num_flashes += 1
                num_flashes += oct_flash_neighbor(oct_map, a, b)
    return num_flashes


def count_flashes(oct_map: List[List[int]], itr: int) -> int:
    num_flashes = 0
    for _ in range(itr):
        for i in range(len(oct_map)):
            for j in range(len(oct_map[i])):
                if oct_map[i][j] == -1:
                    continue
                oct_map[i][j] += 1
                if oct_map[i][j] > 9:
                    oct_map[i][j] = -1
                    num_flashes += oct_flash_neighbor(oct_map, i, j)
                    num_flashes += 1
        for i in range(len(oct_map)):
            for j in range(len(oct_map[i])):
                if oct_map[i][j] == -1:
                    oct_map[i][j] = 0
    return num_flashes


def all_flash_count(oct_map: List[List[int]]) -> int:
    cnt = 0
    while True:
        for i in range(len(oct_map)):
            for j in range(len(oct_map[i])):
                if oct_map[i][j] == -1:
                    continue
                oct_map[i][j] += 1
                if oct_map[i][j] > 9:
                    oct_map[i][j] = -1
                    oct_flash_neighbor(oct_map, i, j)
        sum_flashes = 0
        for i in range(len(oct_map)):
            for j in range(len(oct_map[i])):
                if oct_map[i][j] == -1:
                    oct_map[i][j] = 0
                    sum_flashes += 1
        if sum_flashes == len(oct_map) * len(oct_map[0]):
            return cnt+1
        cnt += 1


def print_oct_map(oct_map: List[List[int]]) -> None:
    print('-'*10)
    for row in oct_map:
        print(''.join(str(c) for c in row))
    print('-'*10)


if __name__ == '__main__':
    oct_map = get_inputs('input.txt')
    print(count_flashes(oct_map, 100))
    oct_map = get_inputs('input.txt')
    print(all_flash_count(oct_map))
