import sys
from enum import Enum
from functools import reduce

VALUE_PACKET_ID = 4
BIT_LENGTH_TYPE = '0'

# Using a global counter so we don't have to use so many substrings and keep
# track of how many bits we've read.
global i
i = 0

def get_next_bits(bin, count):
    global i
    bits = bin[i:i+count]
    i += count
    return bits


global packet_count
packet_count = 0

global packet_version_sum
packet_version_sum = 0

def parse_hex_packet(hex):
    global i
    i = 0

    bin = '{0:08b}'.format(int(hex, 16))

    # Loses leading 0s by default, add them back in
    expected_length = len(hex) * 4
    bin = ''.join(['0'] * (expected_length - len(bin))) + bin

    result = parse_packet(bin)
    print('%s = %s = %d' % (hex, bin, result))
    return result

def parse_packet(bin):
    global packet_count
    global packet_version_sum
    #print('\nParsing packet %s' % bin[i:])

    # Get version
    version = int(get_next_bits(bin, 3), 2)
    type_id = int(get_next_bits(bin, 3), 2)


    packet_count += 1
    packet_version_sum += version

    if type_id == VALUE_PACKET_ID:
        #print('Value packet, version %d' % version)
        return parse_value_packet(bin)
    else:
        #print('Operator packet, version %d' % version)
        packets = parse_operator_packet(bin)
        return exec_operator(type_id, packets)

def exec_operator(packet_type_id, packets):
    if packet_type_id == 0:
        # Sum
        #print('\tSum', packets)
        return sum(packets)
    elif packet_type_id == 1:
        # Product
        #print('\tProduct', packets)
        return reduce(lambda a, b: a * b, packets)
    elif packet_type_id == 2:
        # Minimum
        #print('\tMin', packets)
        return min(packets)
    elif packet_type_id == 3:
        # Maximum
        #print('\tMax', packets)
        return max(packets)
    elif packet_type_id == 5:
        # Greater than
        #print('\tGreater than', packets)
        return 1 if packets[0] > packets[1] else 0
    elif packet_type_id == 6:
        # Less than
        #print('\tLess than', packets)
        return 1 if packets[0] < packets[1] else 0
    elif packet_type_id == 7:
        # Equal to
        #print('\tEqual to', packets)
        return 1 if packets[0] == packets[1] else 0
    else:
        #print('ERROR unknown packet type %d' % packet_type_id)
        return -1

def parse_operator_packet(bin):
    length_type_id = get_next_bits(bin, 1)
    packets = []
    if length_type_id == BIT_LENGTH_TYPE:
        num_bits = int(get_next_bits(bin, 15), 2)
        start_i = i
        end_i = i
        while end_i - start_i < num_bits:
            packets.append(parse_packet(bin))
            end_i = i
    else:
        num_packets = int(get_next_bits(bin, 11), 2)
        for _ in range(num_packets):
            packets.append(parse_packet(bin))
    return packets

def parse_value_packet(bin):
    value_bits = ''

    while True:
        group = get_next_bits(bin, 5)
        value_bits += group[1:]
        prefix = group[0]
        if prefix == '0':
            # Last group
            return int(value_bits, 2)

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        # Run test cases
        assert parse_hex_packet('C200B40A82') == 3
        assert parse_hex_packet('04005AC33890') == 54
        assert parse_hex_packet('880086C3E88112') == 7
        assert parse_hex_packet('CE00C43D881120') == 9
        assert parse_hex_packet('D8005AC2A8F0') == 1
        assert parse_hex_packet('F600BC2D8F') == 0
        assert parse_hex_packet('9C005AC2F8F0') == 0
        assert parse_hex_packet('9C0141080250320F1802104A08') == 1
    else:
        result = parse_hex_packet(sys.argv[1])
        print('Packet Count: %d' % packet_count)
        print('Packet Version Sum: %d' % packet_version_sum)
        print('Result: %d' % result)
