from typing import Tuple, Dict


def get_input(file_name: str) -> Tuple[str, Dict[str, str]]:
    with open(file_name, 'r') as f:
        data = f.readlines()
        original_polymer = data[0].strip()
        rules = {}
        for i in range(2, len(data)):
            data[i] = [x.strip() for x in data[i].split(' -> ')]
            rules[data[i][0]] = data[i][1]
        return original_polymer, rules


def pair_insertion(polymer: str, rules: Dict[str, str], step: int) -> str:
    for itr in range(step):
        new_polymer = ''
        for i in range(len(polymer) - 1):
            if polymer[i:i+2] in rules:
                new_polymer += (polymer[i] + rules[polymer[i:i+2]])
            else:
                new_polymer += polymer[i]
        new_polymer += polymer[-1]
        polymer = new_polymer
        print(itr, len(new_polymer), end='\n')
    return polymer


def most_common_unit(polymer: str) -> int:
    units = {}
    for unit in polymer:
        if unit not in units:
            units[unit] = 0
        units[unit] += 1
    most_common_unit = max(units, key=units.get)
    return units[most_common_unit]


def least_common_unit(polymer: str) -> int:
    units = {}
    for unit in polymer:
        if unit not in units:
            units[unit] = 0
        units[unit] += 1
    least_common_unit = min(units, key=units.get)
    return units[least_common_unit]


def print_rules(rules: Dict[str, str]) -> None:
    for key, value in rules.items():
        print(key, value)


def pair_insertion_optimized(polymer: str, rules: Dict[str, str], step: int) -> str:
    for itr in range(step):
        new_polymer = ''
        for i in range(len(polymer) - 1):
            if polymer[i:i+2] in rules:
                new_polymer += (polymer[i] + rules[polymer[i:i+2]])
            else:
                new_polymer += polymer[i]
        new_polymer += polymer[-1]
        polymer = new_polymer
        print(itr, len(new_polymer), end='\n')
    return polymer


def main() -> None:
    polymer, rules = get_input('input.txt')
    new_polymer = pair_insertion(polymer, rules, 40)
    print(most_common_unit(new_polymer) - least_common_unit(new_polymer))


if __name__ == '__main__':
    main()
