import sys
import math

def process(inputFile):
    max_seat = 0
    plane_seats = [[] for _ in range(128)]
    for line in inputFile:
        row_min = 0
        row_max = 127
        for i in range(7):
            char = line[i]
            midpoint = math.floor((row_min + row_max)/2)
            if char == 'F':
                row_max = midpoint
            elif char == 'B':
                row_min = midpoint + 1
            else:
                print('WARNING: character %s not recognized' % char)
            #print(row_min, row_max)
        assert row_min == row_max
        row = row_min

        col_min = 0
        col_max = 7
        for i in range(3):
            char = line[7+i]
            midpoint = math.floor((col_min + col_max)/2)
            if char == 'L':
                col_max = midpoint
            else:
                col_min = midpoint + 1
            #print (col_min, col_max)
        assert col_min == col_max
        col = col_min

        seat = row * 8 + col
        print("{passport}: row {row}, column {col}, seat ID {seat}".format(
            passport=line.strip(),
            row=row,
            col=col,
            seat=seat
        ))
        if seat > max_seat:
            max_seat = seat

        if not plane_seats[row]:
            plane_seats[row] = [0 for _ in range(8)]

        plane_seats[row][col] = 1

    empty_seats = []
    for row in range(128):
        for col in range(8):
            if not plane_seats[row] or plane_seats[row][col] == 0:
                print("EMPTY - row: {row} col: {col} id: {id}".format(
                    row=row,
                    col=col,
                    id=row * 8 + col
                ))


    print(max_seat)


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        with open(sys.argv[1]) as inputFile:
            process(inputFile)
