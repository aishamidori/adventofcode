from collections import defaultdict
import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        field_defs = {}

        # Class definitions
        while True:
            line = f.readline().strip()
            print(line)

            # On to our ticket
            if line == '':
                break

            colon_split = line.split(': ')
            prop_name = colon_split[0]
            ranges = colon_split[1].split(' or ')
            parsed_ranges = []
            for valid_range in ranges:
                nums = valid_range.split('-')
                parsed_ranges.append((int(nums[0]), int(nums[1])))
            field_defs[prop_name] = parsed_ranges

        # Your ticket
        # Ticket header
        f.readline()

        # Actual numbers
        line = f.readline().strip()
        my_ticket = [int(num) for num in line.split(',')]

        # Blank separator
        f.readline()

        # Nearby tickets
        # Nearby header
        f.readline()

        nearby_tickets = []
        while True:
            line = f.readline().strip()

            # End of file
            if line == '':
                break

            nums = [int(num) for num in line.split(',')]
            nearby_tickets.append(nums)

        print(field_defs)
        print(my_ticket)
        print(nearby_tickets)

    return {
        'field_defs': field_defs,
        'my_ticket': my_ticket,
        'nearby': nearby_tickets
    }

def is_possibly_valid(field_defs, value):
    for val_ranges in field_defs.values():
        for (minval, maxval) in val_ranges:
            if value >= minval and value <= maxval:
                return True
    return False

def is_valid(ranges, value):
    for (minval, maxval) in ranges:
        if value >= minval and value <= maxval:
            return True
    return False

def impossible_indices(field_ranges, ticket):
    impossible_indices = []
    for i in range(len(ticket)):
        if not is_valid(field_ranges, ticket[i]):
            impossible_indices.append(i)
    return impossible_indices

def part1(field_defs, my_ticket, nearby):
    invalid_vals = []
    for ticket in nearby:
        for value in ticket:
            if not is_possibly_valid(field_defs, value):
                invalid_vals.append(value)
    return sum(invalid_vals)

def part2(field_defs, my_ticket, nearby):
    valid_tickets = []
    for ticket in nearby:
        valid = True
        for value in ticket:
            if not is_possibly_valid(field_defs, value):
                valid = False
                break
        if valid:
            valid_tickets.append(ticket)

    num_fields = len(field_defs.keys())
    possible_indices = defaultdict(lambda: list(range(num_fields)))
    for ticket in valid_tickets:
        for (field_name, field_ranges) in field_defs.items():
            impossible = impossible_indices(field_ranges, ticket)
            for val in impossible:
                try:
                    possible_indices[field_name].remove(val)
                except ValueError:
                    pass

    final = postprocess_possible_indices(possible_indices, list(field_defs.keys()))
    result = 1
    for i in range(len(final)):
        if final[i].startswith('departure'):
            print(final[i], my_ticket[i])
            result *= my_ticket[i]

    return result
    #print(possible_indices)

def postprocess_possible_indices(possible_indices, all_fields):
    made_changes = True
    final_ordering = [None for _ in range(len(all_fields))]
    to_order = all_fields[:]

    while made_changes == True:
        made_changes = False
        new_to_order = to_order[:]
        for field in to_order:

            indices = possible_indices[field]

            # We found an assigment!
            if len(indices) == 1:
                final_val = indices[0]
                assert not final_ordering[final_val]
                final_ordering[final_val] = field
                new_to_order.remove(field)

                # Clean the now-reserved value out of the other lists
                for vals in possible_indices.values():
                    if final_val in vals:
                        vals.remove(final_val)

                # Keep iterating now that we've made changes
                made_changes = True

        to_order = new_to_order

    for i in range(len(all_fields)):
        print(i, ':', final_ordering[i])

    return final_ordering


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(**processed))
        print(part2(**processed))
