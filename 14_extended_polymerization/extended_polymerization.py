from typing import Tuple, Dict


def get_input(file_name: str) -> Tuple[str, Dict[str, str]]:
    with open(file_name, 'r') as f:
        data = f.readlines()
        original_polymer = data[0].strip()
        rules = {}
        for i in range(2, len(data)):
            segments = [x.strip() for x in data[i].split(' -> ')]
            rules[segments[0]] = segments[1]
        return original_polymer, rules


def pair_insertion(polymer: str, rules: Dict[str, str], steps: int) -> int:
    for _ in range(steps):
        new_polymer = ''
        for i in range(len(polymer) - 1):
            new_polymer += (polymer[i] + rules[polymer[i:i+2]])
        new_polymer += polymer[-1]
        polymer = new_polymer
    char_counts: Dict[str, int] = {}
    for c in polymer:
        if c in char_counts:
            char_counts[c] += 1
        else:
            char_counts[c] = 1
    return max(char_counts.values()) - min(char_counts.values())


def print_rules(rules: Dict[str, str]) -> None:
    for key, value in rules.items():
        print(key, value)


def pair_insertion_optimized(polymer: str, rules: Dict[str, str], steps: int) -> int:
    pattern_dict: Dict[str, int] = {}
    polymer = '#' + polymer + '#'
    for i in range(len(polymer) - 1):
        if polymer[i:i+2] in pattern_dict:
            pattern_dict[polymer[i:i+2]] += 1
        else:
            pattern_dict[polymer[i:i+2]] = 1
    for _ in range(steps):
        new_pattern_dict: Dict[str, int] = {}
        for key, value in pattern_dict.items():
            if value < 1:
                continue
            if key not in rules:
                if key in new_pattern_dict:
                    new_pattern_dict[key] += value
                else:
                    new_pattern_dict[key] = value
                continue
            insertion = rules[key]
            if key[0]+insertion in new_pattern_dict:
                new_pattern_dict[key[0]+insertion] += value
            else:
                new_pattern_dict[key[0]+insertion] = value
            if insertion+key[1] in new_pattern_dict:
                new_pattern_dict[insertion+key[1]] += value
            else:
                new_pattern_dict[insertion+key[1]] = value
        pattern_dict = new_pattern_dict
    char_counts: Dict[str, int] = {}
    for key, value in pattern_dict.items():
        if key[0] in char_counts:
            char_counts[key[0]] += value
        else:
            char_counts[key[0]] = value
        if key[1] in char_counts:
            char_counts[key[1]] += value
        else:
            char_counts[key[1]] = value
    del char_counts['#']
    max_count = max(char_counts.values()) // 2
    min_count = min(char_counts.values()) // 2
    return max_count - min_count


def main() -> None:
    polymer, rules = get_input('input.txt')
    print(pair_insertion(polymer, rules, 10))
    print(pair_insertion_optimized(polymer, rules, 40))


if __name__ == '__main__':
    main()
