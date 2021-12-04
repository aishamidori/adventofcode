import sys

class Board:
    def __init__(self):
        self.nums = []
        self.markings = []

    def add_row(self, row):
        self.nums += row
        self.markings += [False for _ in range(len(row))]

    def maybe_mark(self, num):
        try:
            i = self.nums.index(num)
            self.markings[i] = True
        except ValueError:
            pass

    def check_win(self):
        for i in range(5):
            if sum(self.markings[(i*5):(i*5)+5]) == 5:
                # Winning row
                return True
            if sum(self.markings[i::5]) == 5:
                # Winning column
                return True
        return False

    def get_score(self):
        sum = 0
        for i in range(len(self.nums)):
            if not self.markings[i]:
                sum += int(self.nums[i])
        return sum

    def __str__(self):
        output = []
        row = []
        for i in range(len(self.nums)):
            if self.markings[i]:
                row.append('\033[91m' + self.nums[i] + '\033[0m')
            else:
                row.append(self.nums[i])

            if i % 5 == 4:
                output.append(row)
                row = []

        return '\n'.join([' '.join(row) for row in output])

def preprocess(file_path):
    boards = []
    with open(file_path) as f:
        nums = f.readline().split(',')
        boards = []
        for line in f:
            stripped = line.strip()
            if stripped == '':
                # Blank line between boards
                boards.append(Board())
            else:
                boards[-1].add_row(stripped.split())

    return (boards, nums)

def part1(processed):
    boards, nums = processed
    for num in nums:
        new_boards = boards[:]
        for board in boards:
            board.maybe_mark(num)
            if board.check_win():
                print("WINNER")
                print(board)
                return board.get_score() * int(num)
        boards = new_boards

def part2(processed):
    boards, nums = processed
    for num in nums:
        new_boards = boards[:]
        for board in boards:
            board.maybe_mark(num)
            if board.check_win():
                print("WINNER")
                print(board)

                # Remove this board since it's won. If it's the last one, it's the one we're looking for
                new_boards.remove(board)
                if not new_boards:
                    return board.get_score() * int(num)
        boards = new_boards

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])

        print('----- PART 1 -----')
        print(part1(processed))

        print('----- PART 1 -----')
        print(part2(processed))
