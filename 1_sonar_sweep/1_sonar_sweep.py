def depth_measurement(str_nums):
    if len(str_nums) <= 1:
        return 0

    cnt = 0
    curr = int(str_nums[0])
    for i in range(1, len(str_nums)):
        if int(str_nums[i]) > curr:
            cnt += 1
        curr = int(str_nums[i])
    return cnt

def depth_measurement_window(str_nums):
    if len(str_nums) <= 3:
        return 0

    cnt = 0
    curr = int(str_nums[0]) + int(str_nums[1]) + int(str_nums[2])
    for i in range(3, len(str_nums)):
        tmp = curr - int(str_nums[i-3]) + int(str_nums[i])
        if tmp > curr:
            cnt += 1
        curr = tmp
    return cnt

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        str_nums = f.readlines()
        print(depth_measurement(str_nums))
        print(depth_measurement_window(str_nums))