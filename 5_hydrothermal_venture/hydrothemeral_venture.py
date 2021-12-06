from typing import Dict, List
def get_inputs(file_name: str) -> List[List[int]]:
    with open(file_name, 'r') as file:
        coor_list = []
        data = file.read().splitlines()
        for line in data:
            segments = line.split()
            coor1 = [int(x) for x in segments[0].split(',')]
            coor2 = [int(x) for x in segments[2].split(',')]
            coor_list.append(coor1+coor2)
        return coor_list

def horizontal_vertical_overlap(coor_list: List[List[int]]) -> int:
    covers: Dict = {}
    for coor in coor_list:
        if coor[0] == coor[2]:
            min_y = min(coor[1], coor[3])
            max_y = max(coor[1], coor[3])
            for i in range(min_y, max_y+1):
                if (coor[0], i) in covers:
                    covers[(coor[0], i)] += 1
                else:
                    covers[(coor[0], i)] = 1
        elif coor[1] == coor[3]:
            min_x = min(coor[0], coor[2])
            max_x = max(coor[0], coor[2])
            for i in range(min_x, max_x+1):
                if (i, coor[1]) in covers:
                    covers[(i, coor[1])] += 1
                else:
                    covers[(i, coor[1])] = 1
    return len([x for x in covers.values() if x > 1])
    
def horizontal_vertical_diagonal_overlap(cover_list: List[List[int]]) -> int:
    covers: Dict = {}
    for coor in cover_list:
        if coor[0] == coor[2]:
            min_y = min(coor[1], coor[3])
            max_y = max(coor[1], coor[3])
            for i in range(min_y, max_y+1):
                if (coor[0], i) in covers:
                    covers[(coor[0], i)] += 1
                else:
                    covers[(coor[0], i)] = 1
        elif coor[1] == coor[3]:
            min_x = min(coor[0], coor[2])
            max_x = max(coor[0], coor[2])
            for i in range(min_x, max_x+1):
                if (i, coor[1]) in covers:
                    covers[(i, coor[1])] += 1
                else:
                    covers[(i, coor[1])] = 1
        else:
            direct_x = 1 if coor[0] < coor[2] else -1
            direct_y = 1 if coor[1] < coor[3] else -1
            distance = coor[2] - coor[0]
            if distance < 0:
                distance = -distance
            for i in range(distance+1):
                tmp_coor = (coor[0] + direct_x*i, coor[1] + direct_y*i)
                if tmp_coor in covers:
                    covers[tmp_coor] += 1
                else:
                    covers[tmp_coor] = 1
    return len([x for x in covers.values() if x > 1])

if __name__ == '__main__':
    coor_list = get_inputs('input.txt')
    print(horizontal_vertical_overlap(coor_list))
    print(horizontal_vertical_diagonal_overlap(coor_list))
