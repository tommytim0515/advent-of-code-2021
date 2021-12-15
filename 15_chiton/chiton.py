import sys
import numpy as np
from queue import PriorityQueue
from typing import List, Tuple

NEIGHBORS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def get_inputs(filename: str) -> List[List[int]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
        return [[int(x) for x in line.strip()] for line in lines]


def lowest_total_risk(risk_map: List[List[int]]) -> int:
    if len(risk_map) == 0:
        return 0
    num_rows = len(risk_map)
    num_cols = len(risk_map[0])
    dijkstra_matrix = [
        [sys.maxsize for _ in range(num_cols)] for _ in range(num_rows)]
    dijkstra_matrix[0][0] = 0
    visited = set()
    pq: PriorityQueue[Tuple[int, int, int]] = PriorityQueue()
    pq.put((0, 0, 0))
    while not pq.empty():
        if (num_rows-1, num_cols-1) in visited:
            break
        _, i, j = pq.get()
        for a, b in NEIGHBORS:
            coor_y = i + a
            coor_x = j + b
            if coor_y < 0 or coor_y >= num_rows or coor_x < 0 or coor_x >= num_cols:
                continue
            if (coor_y, coor_x) in visited:
                continue
            dijkstra_matrix[coor_y][coor_x] = min(dijkstra_matrix[i][j]+risk_map[coor_y][coor_x],
                                                  dijkstra_matrix[coor_y][coor_x])
            new_item = (dijkstra_matrix[coor_y][coor_x], coor_y, coor_x)
            if new_item not in pq.queue:
                pq.put(new_item)
        visited.add((i, j))
    return dijkstra_matrix[num_rows-1][num_cols-1]


def compute_full_map(original_map: List[List[int]]) -> List[List[int]]:
    if len(original_map) == 0:
        return []
    num_rows = len(original_map)
    num_cols = len(original_map[0])
    new_map = [[0 for _ in range(5*num_cols)]
               for _ in range(5*num_rows)]
    for i in range(5):
        for j in range(5):
            for y in range(num_rows):
                for x in range(num_cols):
                    new_val = original_map[y][x] + i + j
                    if new_val > 9:
                        new_val -= 9
                    new_map[y+i*num_rows][x+j * num_cols] = new_val
    return new_map


def main() -> None:
    risk_map = get_inputs('input.txt')
    print(f'Original map: {lowest_total_risk(risk_map)}')
    new_map = compute_full_map(risk_map)
    print(f'Full map: {lowest_total_risk(new_map)}')


if __name__ == '__main__':
    main()
