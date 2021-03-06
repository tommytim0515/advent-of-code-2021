from typing import List, Set, Tuple

START_NOTATION = 'start'
END_NOTATION = 'end'


def get_inputs(filename: str) -> Tuple[List[List[int]], List[str]]:
    with open(filename) as f:
        lines = f.readlines()
    points = set()
    for line in lines:
        two_points = line.strip().split('-')
        for point in two_points:
            if point not in points:
                points.add(point)
    point_list = list(points)
    vertices = [[0 for _ in range(len(point_list))]
                for _ in range(len(point_list))]
    for line in lines:
        two_points = line.strip().split('-')
        vertices[point_list.index(two_points[0])
                 ][point_list.index(two_points[1])] = 1
        vertices[point_list.index(two_points[1])
                 ][point_list.index(two_points[0])] = 1
    return vertices, point_list


def get_num_paths(vertices: List[List[int]], points: List[str], point: str, visited: Set) -> int:
    if point == END_NOTATION:
        return 1
    if point.islower():
        visited.add(point)
    num_paths = 0
    idx = points.index(point)
    for i in range(len(vertices[idx])):
        if vertices[idx][i] == 1 and points[i] not in visited:
            num_paths += get_num_paths(vertices,
                                       points, points[i], visited.copy())
    return num_paths


def get_num_paths_pro(vertices: List[List[int]], points: List[str], point: str, visited: Set, used: bool) -> int:
    if point == END_NOTATION:
        return 1
    if point.islower():
        visited.add(point)
    num_paths = 0
    idx = points.index(point)
    for i in range(len(vertices[idx])):
        if vertices[idx][i] == 0:
            continue
        if points[i] not in visited:
            num_paths += get_num_paths_pro(vertices,
                                           points, points[i], visited.copy(), used)
        elif not used and points[i] != START_NOTATION and points[i] != END_NOTATION:
            num_paths += get_num_paths_pro(vertices,
                                           points, points[i], visited.copy(), True)
    return num_paths


if __name__ == '__main__':
    vertices, points = get_inputs('input.txt')
    for line in vertices:
        print(line)
    print(points)
    print('Number of paths: {}'.format(
        get_num_paths(vertices, points, 'start', set())))
    print('Number of paths pro: {}'.format(
        get_num_paths_pro(vertices, points, 'start', set(), False)))
