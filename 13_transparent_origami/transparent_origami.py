from typing import List, Tuple


def get_inputs(file_name: str) -> Tuple[List[Tuple[int, ...]], List[Tuple[int, ...]]]:
    with open(file_name, 'r') as f:
        data = f.readlines()
        points = []
        idx = 0
        while data[idx].strip() != '':
            points.append(tuple([int(x)
                          for x in data[idx].strip().split(',')]))
            idx += 1
        idx += 1
        folds = []
        while idx < len(data):
            segments = data[idx].strip().split('=')
            if 'x' in data[idx]:
                folds.append(tuple([0, int(segments[-1])]))  # 'x'
            else:
                folds.append(tuple([1, int(segments[-1])]))  # 'y'
            idx += 1
        return points, folds


def first_fold(points: List[Tuple[int, ...]], fold: Tuple[int, ...]) -> int:
    set_points = set()
    if fold[0] == 0:
        for point in points:
            if point[0] > fold[1]:
                set_points.add(tuple([2*fold[1]-point[0], point[1]]))
            else:
                set_points.add(point)
    else:
        for point in points:
            if point[1] > fold[1]:
                set_points.add(tuple([point[0], 2*fold[1]-point[1]]))
            else:
                set_points.add(point)
    return len(list(set_points))


def get_code(points: List[Tuple[int, ...]], folds: List[Tuple[int, ...]]) -> List[List[str]]:
    list_points = points.copy()
    for fold in folds:
        set_points = set()
        if fold[0] == 0:
            for point in list_points:
                if point[0] > fold[1]:
                    set_points.add(tuple([2*fold[1]-point[0], point[1]]))
                else:
                    set_points.add(point)
        else:
            for point in list_points:
                if point[1] > fold[1]:
                    set_points.add(tuple([point[0], 2*fold[1]-point[1]]))
                else:
                    set_points.add(point)
        list_points = list(set_points)
    max_x = max([point[0] for point in list_points])
    min_x = min([point[0] for point in list_points])
    max_y = max([point[1] for point in list_points])
    min_y = min([point[1] for point in list_points])
    matrix = [[' ' for _ in range(max_x-min_x+1)]
              for _ in range(max_y-min_y+1)]
    for point in list_points:
        matrix[point[1]+min_y][point[0]+min_x] = '#'
    return matrix


if __name__ == '__main__':
    points, folds = get_inputs('input.txt')
    print(first_fold(points, folds[0]))
    matrix = get_code(points, folds)
    for row in matrix:
        for col in row:
            print(col, end='')
        print()
