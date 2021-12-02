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
                buses.append((i, int(bus_detail)))
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
    max_bus = (0, 0)
    for bus in processed:
        if bus[1] > max_bus[1]:
            max_bus = bus

    timestamp = max_bus[1] - max_bus[0]
    while True:
        if is_valid(timestamp, processed):
            return timestamp

        timestamp += max_bus[1]
        #print(timestamp)
    return timestamp

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

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        #processed = preprocess(sys.argv[1])
        #print(part1(*processed))

        processed = preprocess2(sys.argv[1])
        print(part2(preprocess2(sys.argv[1])))
        #print(is_valid(1068781, processed))
