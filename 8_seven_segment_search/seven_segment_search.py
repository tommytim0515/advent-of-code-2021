from typing import List, Dict

DIGIT_MAPPING = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}
SEGMENT_SIZE = 7


def pattern_to_num(patterns: List[str], remapping: Dict[str, str]) -> int:
    res = 0
    for pattern in patterns:
        real_pattern = ''.join(sorted([remapping[char] for char in pattern]))
        res *= 10
        res += DIGIT_MAPPING[real_pattern]
    return res


def get_inputs(file_name: str) -> List[List[str]]:
    with open(file_name) as f:
        data = f.readlines()
        res = []
        for line in data:
            parts = [item.strip().split() for item in line.split('|')]
            res.extend(parts)
        return res


def count_occurrence(pattern_list: List[List[str]]) -> int:
    res = 0
    for i in range(0, len(pattern_list), 2):
        for pattern in pattern_list[i+1]:
            # numbers of segments for presenting 1, 7, 4, and 8 are unique
            if len(pattern) in (2, 3, 4, 7):
                res += 1
    return res


def solve_digits(pattern_list: List[List[str]]) -> int:
    total = 0
    for i in range(0, len(pattern_list), 2):
        mapping = {}
        order_by_len: List[List[str]] = [[] for _ in range(SEGMENT_SIZE+1)]
        for pattern in pattern_list[i]:
            order_by_len[len(pattern)].append(pattern)

        # find 'a'
        set_1 = set(order_by_len[2][0])
        set_7 = set(order_by_len[3][0])
        mapping['a'] = list(set_7 - set_1)[0]

        # find 'g'
        set_4 = set(order_by_len[4][0])
        for pattern in order_by_len[6]:
            set_pattern = set(pattern)
            if set_4.issubset(set_pattern):
                set_pattern -= set_4
                set_pattern.remove(mapping['a'])
                mapping['g'] = list(set_pattern)[0]
                break

        # find 'd'
        for pattern in order_by_len[5]:
            set_pattern = set(pattern)
            if set_1.issubset(set_pattern):
                set_pattern -= set_1
                set_pattern -= {mapping[c] for c in ('a', 'g')}
                mapping['d'] = list(set_pattern)[0]
                break

        # find 'b'
        set_4 -= set_1
        set_4.remove(mapping['d'])
        mapping['b'] = list(set_4)[0]

        # find 'e'
        for pattern in order_by_len[6]:
            if mapping['d'] not in pattern:
                set_pattern = set(pattern)
                set_pattern -= set_1
                set_pattern -= {mapping[c] for c in ('a', 'b', 'g')}
                mapping['e'] = list(set_pattern)[0]
                break

        # find 'f'
        for pattern in order_by_len[6]:
            set_pattern = set(pattern)
            if set([mapping['b'], mapping['d'], mapping['e']]).issubset(set_pattern):
                set_pattern -= {mapping[c] for c in ('a', 'b', 'd', 'e', 'g')}
                mapping['f'] = list(set_pattern)[0]
                break

        # find part 'c'
        set_1.remove(mapping['f'])
        mapping['c'] = list(set_1)[0]

        reverse_mapping = {v: k for k, v in mapping.items()}
        total += pattern_to_num(pattern_list[i+1], reverse_mapping)
    return total


if __name__ == '__main__':
    pattern_list = get_inputs('input.txt')
    print(f'Occurrence of 1, 4, 7, 8: {count_occurrence(pattern_list)}')
    print(f'Sum of real numbers: {solve_digits(pattern_list)}')
