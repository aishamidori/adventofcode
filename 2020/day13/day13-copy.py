import math
import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        earliest_time = int(f.readline())

        bus_details = f.readline().split(',')
        buses = []
        for bus_detail in bus_details:
            if bus_detail == 'x':
                continue
            else:
                buses.append(int(bus_detail))
    return (earliest_time, buses)

def preprocess2(file_path):
    processed = []
    with open(file_path) as f:
        earliest_time = int(f.readline())

        bus_details = f.readline().split(',')
        buses = []
        for i in range(len(bus_details)):
            bus_detail = bus_details[i]
            if bus_detail == 'x':
                continue
            else:
                bus_id = int(bus_detail)
                buses.append(((bus_id - i) % bus_id, bus_id))
        #print(buses)
    return buses

def part1(earliest_time, buses):
    bus_times = []
    for bus in buses:
        iterations = math.ceil(earliest_time / bus)
        arrival_time = iterations * bus
        bus_times.append({
            'time': arrival_time,
            'bus_id': bus
        })
    bus_times.sort(key=lambda time: time['time'])
    best_bus = bus_times[0]
    return (best_bus['time'] - earliest_time) * best_bus['bus_id']

def part2(processed):
    max_to_check = 1
    for bus in processed:
        print(bus)
        max_to_check *= bus[1]
    print(max_to_check)

    for timestamp in range(max_to_check, int(max_to_check/2), -1):
        if is_valid(timestamp, processed):
            return timestamp

    return timestamp

def part2again(processed):
    processed.sort(key=lambda bus: -bus[1])
    num = processed[0][0] + processed[0][1]
    to_add = processed[0][1]

    for i in range(len(processed) - 1):
        bus = processed[i]
        next_bus = processed[i+1]

        print('Bus:', bus)
        #print('next_bus:', next_bus)
        while True:
            if num % next_bus[1] == next_bus[0]:
                print('Found it - %d mod %d -> %d (looking for %d)' % (num, next_bus[1], num % next_bus[1], next_bus[0]))
                print('Continuing from', num)
                break
                #print('Haven\'t found it yet - %d mod %d -> %d (looking for %d)' % (num, next_bus[1], num % next_bus[1], next_bus[0]))

            num += to_add

        to_add *= next_bus[1]
        print('Updated to_add to', to_add)
    return num

def is_valid(timestamp, buses):
    #print(timestamp)
    correct = True
    for (delay, bus) in buses:
        #print('\n', timestamp, delay, bus)
        #print((timestamp + delay) % bus, '=', 0)
        if (timestamp + delay) % bus != 0:
            correct = False
            break
    return correct


def lcm_multiple(integers):
    total = 1
    for integer in integers:
            total *= integer
    gcd = reduce(math.gcd, integers)
    return total // gcd

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        #processed = preprocess(sys.argv[1])
        #print(part1(*processed))

        processed = preprocess2(sys.argv[1])
        #print(part2(preprocess2(sys.argv[1])))
        #print(is_valid(1068781, processed))
        print('FINAL ANSWER', part2again(processed))
