import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        for line in f:
            pass
    return processed

def part1(file_path):
    tot_sum = 0
    with open(file_path) as f:
        for line in f:
            print('---------------------------------------')
            tot_sum += solve(line.strip())
    return tot_sum

def solve(equation):
    #print("solve", equation)
    i = len(equation) - 1
    first_num = None
    while i >= 0:
        char = equation[i]
        if char == ' ':
            pass
        elif char in ('+', '*', '-', '/'):
            result = do_op(char, first_num, solve(equation[:i - 1]))
            print("Finished solving", first_num, char, equation[:i - 1], " got", result)
            return result
        elif char == ')':
            start_i = find_left_paren(equation, i)
            assert not first_num
            #print("Solving parenthetical", equation[start_i + 1:i])
            first_num = solve(equation[start_i + 1:i])
            #print('Evaluated parenthetical', first_num)
            i = start_i - 1
        else:
            #print(char)
            assert char.isnumeric()
            if not first_num:
                first_num = int(char)
            else:
                print('not sure what to do with', char)
        i -= 1

    return first_num

def part2(file_path):
    tot_sum = 0
    with open(file_path) as f:
        for line in f:
            print('---------------------------------------')
            tot_sum += solve2(line.strip())
    return tot_sum

def solve2(equation):
    print("Starting to solve", equation)
    i = len(equation) - 1
    first_num = None
    while i >= 0:
        char = equation[i]
        if char == ' ':
            pass
        elif char == '*':
            print(first_num, char, '(', equation[:i-1], ')')
            result = do_op(char, first_num, solve2(equation[:i - 1]))
            print("Finished solving", first_num, char, equation[:i - 1], " got", result)
            return result
        elif char == '+':
            if equation[i - 2].isnumeric():
                old_first = first_num
                first_num = do_op(char, first_num, int(equation[i - 2]))
                print("Finished solving", old_first, char, equation[i - 2], " got", first_num)
                i = i - 3
            elif equation[i - 2] == ')':
                start_i = find_left_paren(equation, i - 2)
                old_first = first_num
                first_num = do_op(char, first_num, solve2(equation[start_i + 1:i - 2]))
                print("Finished solving", old_first, char, equation[start_i + 1:i - 2], " got", first_num)
                i = start_i - 1
        elif char == ')':
            start_i = find_left_paren(equation, i)
            assert not first_num
            #print("Solving parenthetical", equation[start_i + 1:i])
            first_num = solve2(equation[start_i + 1:i])
            #print('Evaluated parenthetical', first_num)
            i = start_i - 1
        else:
            #print(char)
            assert char.isnumeric()
            if not first_num:
                first_num = int(char)
            else:
                print('not sure what to do with', char)
        i -= 1

    return first_num

def find_right_paren(equation, lparen_i):
    i = lparen_i + 1
    internal_close_count = 0
    while i < len(equation):
        char = equation[i]
        if char == '(':
            internal_close_count += 1
        elif char == ')':
            if internal_close_count > 0:
                internal_close_count -= 1
            else:
                return i
        i += 1

    print('Couldn\'t find an open paren in', equation)

def find_left_paren(equation, close_i):
    i = close_i - 1
    internal_close_count = 0
    while i >= 0:
        char = equation[i]
        if char == ')':
            internal_close_count += 1
        elif char == '(':
            if internal_close_count > 0:
                internal_close_count -= 1
            else:
                return i
        i -= 1
    print('Couldn\'t find an open paren in', equation)



def do_op(operation, first_num, second_num):
    print(first_num, operation, second_num)
    if operation == '+':
        return first_num + second_num
    elif operation == '-':
        return first_num - second_num
    elif operation == '*':
        return first_num * second_num
    elif operation == '/':
        return first_num / second_num

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        #processed = preprocess(sys.argv[1])
        #print(part1(sys.argv[1]))
        print(part2(sys.argv[1]))
