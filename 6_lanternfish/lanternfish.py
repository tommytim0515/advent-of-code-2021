from typing import List

def get_inputs(file_name: str) -> List[int]:
    with open(file_name, 'r') as f:
        data = f.read().split(',')
        return [int(x) for x in data]

def lanternfish_iteration(fish_list: List[int], days: int) -> int:
    for _ in range(days):
        addition = 0
        for i in range(len(fish_list)):
            if fish_list[i] == 0:
                fish_list[i] = 6
                addition += 1
            else:
                fish_list[i] -= 1                
        fish_list += [8 for _ in range(addition)]
    return len(fish_list)

def lanternfish_iteration_optimized(fish_list: List[int], days: int) -> int:
    iter_list = [0 for _ in range(9)]
    for fish in fish_list:
        iter_list[fish] += 1
    for _ in range(days):
        addition = iter_list[0]
        for i in range(8):
            iter_list[i] = iter_list[i + 1]
        iter_list[-1] = addition
        iter_list[6] += addition
    return sum(iter_list)


if __name__ == '__main__':
    fish_list = get_inputs('input.txt')
    print(lanternfish_iteration_optimized(fish_list, 256))