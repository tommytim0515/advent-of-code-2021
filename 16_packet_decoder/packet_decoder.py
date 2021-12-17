from typing import Tuple, List

MAP_HEX_TO_BINARY = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}
LEN_PACKET_VERSION = 3
LEN_PACKET_TYPE = 3
LEN_PACKET_ID = 1
LEN_NUM_REPRESENTATIONS = {
    0: 15,
    1: 11,
}
TYPE_PACKET_SUM = 0
TYPE_PACKET_PRODUCT = 1
TYPE_PACKET_MINIMUM = 2
TYPE_PACKET_MAXIMUM = 3
TYPE_PACKET_LITERAL_VALUE = 4
TYPE_PACKET_GREATER_THAN = 5
TYPE_PACKET_LESS_THAN = 6
TYPE_PACKET_EQUAL = 7
LENGTH_TYPE_ID_TOTAL_LEN_IN_BITS = 0


def operator_sum(literal_values: List[int]) -> int:
    return sum(literal_values)


def operator_product(literal_values: List[int]) -> int:
    res = 1
    for value in literal_values:
        res *= value
    return res


def operator_min(literal_values: List[int]) -> int:
    return min(literal_values)


def operator_max(literal_values: List[int]) -> int:
    return max(literal_values)


def operator_greater_than(literal_values: List[int]) -> int:
    return 1 if literal_values[0] > literal_values[1] else 0


def operator_less_than(literal_values: List[int]) -> int:
    return 1 if literal_values[0] < literal_values[1] else 0


def operator_equal(literal_values: List[int]) -> int:
    return 1 if literal_values[0] == literal_values[1] else 0


MAP_OPERATOR = {
    TYPE_PACKET_SUM: operator_sum,
    TYPE_PACKET_PRODUCT: operator_product,
    TYPE_PACKET_MINIMUM: operator_min,
    TYPE_PACKET_MAXIMUM: operator_max,
    TYPE_PACKET_GREATER_THAN: operator_greater_than,
    TYPE_PACKET_LESS_THAN: operator_less_than,
    TYPE_PACKET_EQUAL: operator_equal,
}


def get_input(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def hex_to_binary(hex_str: str) -> str:
    binary_str = ''
    for char in hex_str:
        binary_str += MAP_HEX_TO_BINARY[char]
    return binary_str


def binary_to_decimal(binary_str: str) -> Tuple[int, int]:
    decimal_int = 0
    for char in binary_str:
        decimal_int = decimal_int * 2 + int(char)
    return decimal_int


def decode_literal_value(binary_str: str, idx: int) -> Tuple[int, int]:
    prev_idx = idx
    num_str = ''
    while True:
        num_str += binary_str[idx+1:idx+5]
        if binary_str[idx] == '0':
            break
        idx += 5
    idx += 5
    return idx, binary_to_decimal(num_str)


def decode_operator_by_len(binary_str: str, idx: int, length: int) -> Tuple[int, int, List[int]]:
    prev_idx = idx
    sum_versions = 0
    values = []
    while True:
        idx, version, value = decode_packet(binary_str, idx)
        sum_versions += version
        values.append(value)
        if (idx - prev_idx) >= length:
            break
    return idx, sum_versions, values


def decode_operator_by_num(binary_str: str, idx: int, num: int) -> Tuple[int, int, List[int]]:
    cnt = 0
    sum_versions = 0
    values = []
    while True:
        idx, version, value = decode_packet(binary_str, idx)
        sum_versions += version
        values.append(value)
        cnt += 1
        if cnt >= num:
            break
    return idx, sum_versions, values


def decode_operator(binary_str: str, idx: int) -> Tuple[int, int, List[int]]:
    length_type_id = binary_to_decimal(binary_str[idx:idx+LEN_PACKET_ID])
    print(f'Length type id: {length_type_id}')
    idx += LEN_PACKET_ID
    len_num_representation = LEN_NUM_REPRESENTATIONS[length_type_id]
    num_representation = binary_to_decimal(
        binary_str[idx:idx+len_num_representation])
    idx += len_num_representation
    sum_versions = 0
    values = []
    if length_type_id == LENGTH_TYPE_ID_TOTAL_LEN_IN_BITS:
        print(f'Size subpackets: {num_representation}')
        idx, sum_versions, values = decode_operator_by_len(
            binary_str, idx, num_representation)
    else:
        print(f'Num subpackets: {num_representation}')
        idx, sum_versions, values = decode_operator_by_num(
            binary_str, idx, num_representation)
    return idx, sum_versions, values


def decode_packet(binary_str: str, idx: int) -> Tuple[int, int, int]:
    if idx >= len(binary_str):
        raise ValueError('Index larger than string length')
    packet_version = binary_to_decimal(binary_str[idx:idx+LEN_PACKET_VERSION])
    idx += LEN_PACKET_VERSION
    packet_type = binary_to_decimal(binary_str[idx:idx+LEN_PACKET_TYPE])
    idx += LEN_PACKET_TYPE
    sum_versions = 0
    value = 0
    print(f'[idx: {idx}, version: {packet_version}, type: {packet_type}]')
    if packet_type == TYPE_PACKET_LITERAL_VALUE:
        idx, value = decode_literal_value(binary_str, idx)
        print(f'Literal value: {value}')
    else:
        idx, sum_versions, values = decode_operator(binary_str, idx)
        value = MAP_OPERATOR[packet_type](values)
    return idx, packet_version + sum_versions, value


def main() -> None:
    hex_str = get_input('input.txt')
    binary_str = hex_to_binary(hex_str)
    _, sum_versions, result = decode_packet(binary_str, 0)
    print(f'Sum versions: {sum_versions}')
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
