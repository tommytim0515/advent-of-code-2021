HEX_TO_BINARY_MAPPING = {
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


def get_input(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()

def decode_packet(hex_str: str) -> str:
    binary_str = ''
    for char in hex_str:
        binary_str += HEX_TO_BINARY_MAPPING[char]
    print(binary_str)
    return binary_str

def main() -> None:
    hex_str = get_input('input.txt')
    binary_str = decode_packet(hex_str)
    print(binary_str)

if __name__ == '__main__':
    main()
