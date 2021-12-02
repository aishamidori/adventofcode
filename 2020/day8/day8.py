import sys

def preprocess(file_path):
    instructions = []
    with open(file_path) as f:
        for line in f:
            instruction = line.split(' ')
            instructions.append([instruction[0], int(instruction[1])])
    return instructions

def get_value(instructions):
    value = 0
    index = 0
    visited = set()
    switch_used = False
    while index < len(instructions):
        old_index = index

        #print('index:', index, 'value:', value)
        instruction = instructions[index]
        visited.add(index)

        print(instruction)
        if instruction[0] == 'nop':
            index = index + 1
        elif instruction[0] == 'acc':
            index = index + 1
            value = value + instruction[1]
        elif instruction[0] == 'jmp':
            index = index + instruction[1]
        else:
            print("ERROR")


        if index in visited:
            print('Hit an infinite loop')
            return None

        #print('visited:', visited)

        #print('next:', index, '\n')
        continue
    return value


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        instructions = preprocess(sys.argv[1])
        for i in range(len(instructions)):
            if instructions[i][0] == 'jmp':
                # Make a modifiable copy of the instructions
                copy = instructions[:]
                new_inst = copy[i][:]
                new_inst[0] = 'nop'
                copy[i] = new_inst

                result = get_value(copy)
                if result is not None:
                    print("Got a valid result:", result)
                    break
