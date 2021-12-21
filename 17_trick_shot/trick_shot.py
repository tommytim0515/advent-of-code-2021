from typing import Tuple, Set

ACCELERATION_X = -1
ACCELERATION_Y = -1
VELOCITY_Y_RANGE = 1000
TIME_RANGE = 1000


def get_inputs(filename: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    with open(filename, 'r') as f:
        data = f.read()
        segments = data.split(', ')
        segment_x = segments[-2].split('=')
        segment_x = segment_x[1].split('..')
        segment_y = segments[-1].split('=')
        segment_y = segment_y[1].split('..')
        return (int(segment_x[0]),
                int(segment_x[1])), (int(segment_y[0]), int(segment_y[1]))


def trajectory_emulation(velocity_x: int, velocity_y: int, time: int) -> Tuple[int, int]:
    coor_x = 0
    tmp = abs(velocity_x // ACCELERATION_X)
    if time > tmp:
        coor_x = velocity_x * tmp + ACCELERATION_X * tmp * (tmp - 1) // 2
    else:
        coor_x = velocity_x * time + \
            ACCELERATION_X * time * (time - 1) // 2
    coor_y = velocity_y * time + ACCELERATION_Y * time * (time - 1) // 2
    return coor_x, coor_y


def get_maximum_height(velocity_y: int, time: int) -> int:
    max_time = abs(velocity_y // ACCELERATION_Y)
    if time >= max_time:
        return velocity_y * max_time + ACCELERATION_Y * max_time * (max_time - 1) // 2
    else:
        return velocity_y * time + ACCELERATION_Y * time * (time - 1) // 2


def find_maximum_height(range_x: Tuple[int, int], range_y: Tuple[int, int]) -> int:
    max_velocity_x = range_x[1]
    min_velocity_y = range_y[0]
    valid_velocity_x = []
    for v in range(1, max_velocity_x + 1):
        max_tmp_t = abs(v // ACCELERATION_X)
        for t in range(1, max_tmp_t + 1):
            coor_x, _ = trajectory_emulation(v, 0, t)
            if coor_x >= range_x[0] and coor_x <= range_x[1]:
                valid_velocity_x.append(v)
    max_height = range_y[0] - 1
    # brute force solution :/
    for v_x in valid_velocity_x:
        for v_y in range(min_velocity_y, VELOCITY_Y_RANGE + 1):
            for t in range(TIME_RANGE):
                coor_x, coor_y = trajectory_emulation(v_x, v_y, t)
                if coor_x >= range_x[0] and coor_x <= range_x[1] and \
                        coor_y >= range_y[0] and coor_y <= range_y[1]:
                    max_height = max(max_height, get_maximum_height(v_y, t))
    if max_height < range_y[0]:
        return -1
    return max_height


def count_distinct_init_velocity(range_x: Tuple[int, int], range_y: Tuple[int, int]) -> int:
    max_velocity_x = range_x[1]
    min_velocity_y = range_y[0]
    valid_velocity_x = []
    cnt = 0
    for v in range(1, max_velocity_x + 1):
        max_tmp_t = abs(v // ACCELERATION_X)
        for t in range(1, max_tmp_t + 1):
            coor_x, _ = trajectory_emulation(v, 0, t)
            if coor_x >= range_x[0] and coor_x <= range_x[1]:
                valid_velocity_x.append([v, t])
                break
    for v_x, v_x_t in valid_velocity_x:
        for v_y in range(min_velocity_y, VELOCITY_Y_RANGE):
            for t in range(v_x_t, TIME_RANGE):
                coor_x, coor_y = trajectory_emulation(v_x, v_y, t)
                if coor_x >= range_x[0] and coor_x <= range_x[1] and \
                        coor_y >= range_y[0] and coor_y <= range_y[1]:
                    cnt += 1
                    break
    return cnt


def main() -> None:
    range_x, range_y = get_inputs('input.txt')
    print(range_x, range_y)
    print(find_maximum_height(range_x, range_y))
    print(count_distinct_init_velocity(range_x, range_y))

if __name__ == '__main__':
    main()
