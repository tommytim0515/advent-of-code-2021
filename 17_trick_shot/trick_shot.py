from typing import Tuple


def get_inputs(filename: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    with open(filename, 'r') as f:
        data = f.read()
        segments = data.split(', ')
        segment_x = segments[-2].split('=')
        segment_x = segment_x[1].split('..')
        segment_y = segments[-1].split('=')
        segment_y = segment_y[1].split('..')
        return (int(segment_x[0]), int(segment_x[1])), \
            (int(segment_y[0]), int(segment_y[1]))


def main() -> None:
    pass


if __name__ == '__main__':
    range_x, range_y = get_inputs('input.txt')
    print(range_x, range_y)
