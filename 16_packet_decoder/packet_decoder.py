import enum
import math
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
TYPE_TOTAL_LEN_IN_BITS = 0


class TYPE_PACKET(enum.Enum):
    summarize = 0
    product = 1
    minimum = 2
    maximum = 3
    literal_value = 4
    greater_than = 5
    less_than = 6
    equal_to = 7


MAP_OPERATOR = {
    TYPE_PACKET.summarize: (lambda literal_values: sum(literal_values)),
    TYPE_PACKET.product: (lambda literal_values: math.prod(literal_values)),
    TYPE_PACKET.minimum: (lambda literal_values: min(literal_values)),
    TYPE_PACKET.maximum: (lambda literal_values: max(literal_values)),
    TYPE_PACKET.greater_than: (lambda literal_values:
                               1 if literal_values[0] > literal_values[1] else 0),
    TYPE_PACKET.less_than: (lambda literal_values:
                            1 if literal_values[0] < literal_values[1] else 0),
    TYPE_PACKET.equal_to: (lambda literal_values:
                           1 if literal_values[0] == literal_values[1] else 0),
}


def get_input(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def hex_to_binary(hex_str: str) -> str:
    binary_str = ''
    for char in hex_str:
        binary_str += MAP_HEX_TO_BINARY[char]
    return binary_str


def binary_to_decimal(binary_str: str) -> int:
    decimal_int = 0
    for char in binary_str:
        decimal_int = decimal_int * 2 + int(char)
    return decimal_int


def decode_literal_value(binary_str: str, idx: int) -> Tuple[int, int]:
    num_str = ''
    while True:
        num_str += binary_str[idx+1:idx+5]
        idx += 5
        if binary_str[idx-5] == '0':
            break
    return idx, binary_to_decimal(num_str)


def decode_operator_by_len(binary_str: str, idx: int, length: int) -> Tuple[int, int, List[int]]:
    prev_idx = idx
    sum_versions = 0
    values: List[int] = []
    while idx - prev_idx < length:
        idx, version, value = decode_packet(binary_str, idx)
        sum_versions += version
        values.append(value)
    return idx, sum_versions, values


def decode_operator_by_num(binary_str: str, idx: int, num: int) -> Tuple[int, int, List[int]]:
    cnt = 0
    sum_versions = 0
    values = []
    while cnt < num:
        idx, version, value = decode_packet(binary_str, idx)
        sum_versions += version
        values.append(value)
        cnt += 1
    return idx, sum_versions, values


def decode_operator(binary_str: str, idx: int) -> Tuple[int, int, List[int]]:
    length_type_id = binary_to_decimal(binary_str[idx:idx+LEN_PACKET_ID])
    # print(f'Length type id: {length_type_id}')
    idx += LEN_PACKET_ID
    len_num_representation = LEN_NUM_REPRESENTATIONS[length_type_id]
    num_representation = binary_to_decimal(
        binary_str[idx:idx+len_num_representation])
    idx += len_num_representation
    sum_versions = 0
    values: List[int]= []
    if length_type_id == TYPE_TOTAL_LEN_IN_BITS:
        # print(f'Size subpackets: {num_representation}')
        idx, sum_versions, values = decode_operator_by_len(
            binary_str, idx, num_representation)
    else:
        # print(f'Num subpackets: {num_representation}')
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
    # print(f'[idx: {idx}, version: {packet_version}, type: {packet_type}]')
    if TYPE_PACKET(packet_type) == TYPE_PACKET.literal_value:
        idx, value = decode_literal_value(binary_str, idx)
        # print(f'Literal value: {value}')
    else:
        idx, sum_versions, values = decode_operator(binary_str, idx)
        value = MAP_OPERATOR[TYPE_PACKET(packet_type)](values)
    return idx, packet_version + sum_versions, value


def main() -> None:
    hex_str = get_input('input.txt')
    binary_str = hex_to_binary(hex_str)
    _, sum_versions, result = decode_packet(binary_str, 0)
    print(f'Sum versions: {sum_versions}')
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
