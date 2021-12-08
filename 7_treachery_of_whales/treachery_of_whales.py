import sys
import statistics
from typing import List

def get_inputs(file_name: str) -> List[int]:
    with open(file_name, 'r') as f:
        inputs = f.read()
    return [int(i) for i in inputs.split(',')]

def alignment_cost(crab_list: List[int], pivot: int) -> int:
    cost = 0
    for crab in crab_list:
        tmp = abs(crab - pivot)
        cost += tmp * (tmp + 1) // 2
    return cost

def minimum_cost_alignment(crab_list: List[int]) -> int:
    median = int(statistics.median(crab_list))
    cost = 0
    for crab in crab_list:
        cost += abs(crab - median)
    return cost
    
def minimum_cost_alignment_modified(crab_list: List[int]) -> int:
    min_val = min(crab_list)
    max_val = max(crab_list)
    # cost is the maximum integer
    cost = sys.maxsize
    pivot = 0
    for i in range(min_val, max_val + 1):
        if alignment_cost(crab_list, i) < cost:
            cost = alignment_cost(crab_list, i)
            pivot = i
    print(f'Pivot: {pivot}')
    return cost

def minimum_cost_alignment_gradient_descent(crab_list: List[int]) -> int:
    min_val = min(crab_list)
    max_val = max(crab_list)

    

if __name__ == '__main__':
    crab_list = get_inputs('input.txt')
    print(minimum_cost_alignment(crab_list))
    print(minimum_cost_alignment_modified(crab_list))