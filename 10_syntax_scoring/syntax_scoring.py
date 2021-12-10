import statistics
from typing import List

SET_NOTATIONS = set([')', ']', '}', '>'])
NOTATION_MAPPING = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
WRONG_NOTATION_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
COMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def get_inputs(file_name: str) -> List[str]:
    with open(file_name, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def syntax_error_score(lines: List[str]) -> int:
    score = 0
    for line in lines:
        stack = []
        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                stack.append(char)
            else:
                if len(stack) > 0 and stack[-1] == NOTATION_MAPPING[char]:
                    stack.pop()
                else:
                    stack.append(char)
        if len(stack) == 0:
            continue
        set_stack = set(stack)
        if len(set_stack.intersection(SET_NOTATIONS)) == 0:
            continue
        wrong_notations = list(set_stack.intersection(SET_NOTATIONS))
        min_idx = len(stack)
        wrong_notation = wrong_notations[0]
        for notation in wrong_notations:
            idx = stack.index(notation)
            if idx < min_idx:
                min_idx = idx
                wrong_notation = notation
        score += WRONG_NOTATION_SCORE[wrong_notation]
    return score


def fix_incomplete(lines: List[str]) -> int:
    scores = []
    for line in lines:
        stack = []
        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                stack.append(char)
            else:
                if len(stack) > 0 and stack[-1] == NOTATION_MAPPING[char]:
                    stack.pop()
                else:
                    stack.append(char)
        if len(stack) == 0:
            continue
        set_stack = set(stack)
        if len(set_stack.intersection(SET_NOTATIONS)) != 0:
            continue
        addition = []
        for i in range(len(stack)-1, -1, -1):
            char = stack[i]
            addition.append(NOTATION_MAPPING[char])
        score = 0
        for char in addition:
            score *= 5
            score += COMPLETE_SCORE[char]
        scores.append(score)
    return int(statistics.median(scores))


if __name__ == '__main__':
    data = get_inputs('input.txt')
    print(f'Err score: {syntax_error_score(data)}')
    print(f'Incomplete score: {fix_incomplete(data)}')
