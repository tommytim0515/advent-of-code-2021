class submarine:
    def __init__(self):
        self.horizontal_position = 0
        self.vertical_position = 0
        self.aim = 0
    
    def change_position(self, direction: str, distance: str) -> None:
        if direction == 'forward':
            self.vertical_position += int(distance)
        elif direction == 'up':
            self.horizontal_position -= int(distance)
        elif direction == 'down':
            self.horizontal_position += int(distance)

    def change_position_with_aim(self, direction: str, distance: str) -> None:
        if direction == 'forward':
            self.vertical_position += int(distance)
            self.horizontal_position += int(distance) * self.aim
        elif direction == 'up':
            self.aim -= int(distance)
        elif direction == 'down':
            self.aim += int(distance)

    def get_position(self) -> str:
        return f'{self.horizontal_position}, {self.vertical_position}'

    def get_multiplication(self) -> int:
        return self.horizontal_position * self.vertical_position

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        instructions = f.readlines()
        print('change position')
        s1 = submarine()
        for instruction in instructions:
            direction, distance = instruction.split()
            s1.change_position(direction, distance)
        print(s1.get_position())
        print(s1.get_multiplication())

        print('change position with aim')
        s2 = submarine()
        for instruction in instructions:
            direction, distance = instruction.split()
            s2.change_position_with_aim(direction, distance)
        print(s2.get_position())
        print(s2.get_multiplication())