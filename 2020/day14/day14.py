import re
import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            pass
    return processed

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def part1(file_path):
    with open(file_path) as f:
        memory = {}
        curr_mask = ['X' for _ in range(36)]
        for line in f:
            #print('\n', line)
            split = line.split(' = ')
            operation = split[0]
            value = split[1]
            if operation[:4] == 'mask':
                curr_mask = list(value.strip())
                #print('New mask', curr_mask)
            elif operation[:3] == 'mem':
                #print(re.split('\[\]', operation))
                index = int(re.split('\[|\]', operation)[1])
                num = int(value.strip())
                num_with_mask = apply_mask(num, curr_mask)
                #print('mem set of', index, ' - new value is', num_with_mask)
                memory[index] = num_with_mask
                #print('with mask:', num_with_mask)
        print(memory)
        return sum(memory.values())


def apply_mask(initial_number, current_mask):
    #print('\nAPPLYING', ''.join(str(char) for char in current_mask))
    number = initial_number
    #print("before", number, '-', bin(number))
    i = 35
    for mask_val in current_mask:
        #print('index', i, 'mask_val =', mask_val)
        if mask_val == 'X':
            pass
        elif mask_val == 'Y':
            pass
        elif int(mask_val) == 0:
            number = clear_bit(number, i)
            #print('cleared bit', i, 'new number =', number)
        elif int(mask_val) == 1:
            number = set_bit(number, i)
            #print('set bit', i, 'new number =', number)
        i -= 1
    #print("after", number, '-', bin(number))
    return number

def apply_mask2(initial_number, current_mask):
    #print('MASKS:', masks)
    new_numbers = []
    for mask in masks:
        i = 35
        number = initial_number
        for mask_val in mask:
            #print('index', i, 'mask_val =', mask_val)
            if mask_val == 'X':
                #print("ERROR: mask not properly cleaned")
                pass
            elif int(mask_val) == 0:
                number = clear_bit(number, i)
                #print('cleared bit', i, 'new number =', number)
            elif int(mask_val) == 1:
                number = set_bit(number, i)
                #print('set bit', i, 'new number =', number)
            i -= 1
        new_numbers.append(number)
    return new_numbers

def get_all_masks(mask):
    if not 'X' in mask:
        #print('base case -', ''.join(str(val) for val in mask))
        return [mask]

    i = 35
    new_numbers = []
    for i in range(35, -1, -1):
        #print('index', i, 'mask_val =', mask_val)
        mask_val = mask[i]
        if mask_val == 'X':
            #print("trying values at index", i)
            mask_0 = mask[:]
            mask_0[i] = 0
            new_numbers += get_all_masks(mask_0)
            #print('new_numbers', new_numbers)

            mask_1 = mask[:]
            mask_1[i] = 1
            new_numbers += get_all_masks(mask_1)
            #print('new_numbers', new_numbers)
            break
        else:
            pass
        i -= 1

    return new_numbers


def part2(file_path):
    with open(file_path) as f:
        memory = {}
        curr_masks = []
        for line in f:
            split = line.split(' = ')
            operation = split[0]
            value = split[1]
            if operation[:4] == 'mask':
                raw_mask = value.strip().replace('0', 'Y')
                curr_masks = get_all_masks(list(raw_mask))
            elif operation[:3] == 'mem':
                raw_index = int(re.split('\[|\]', operation)[1])
                num = int(value.strip())
                for mask in curr_masks:
                    index_with_mask = apply_mask(raw_index, mask)
                    memory[index_with_mask] = num
        print(memory)
        return sum(memory.values())

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(sys.argv[1]))
        print(part2(sys.argv[1]))
