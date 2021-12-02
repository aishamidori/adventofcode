import sys

def preprocess(file_path):
    rules = {}
    messages = []
    with open(file_path) as f:
        for line in f:
            if line == '\n':
                break

            rule = line.strip().split(': ')
            #print(rule)
            rules[int(rule[0])] = parse_rule_def(rule[1])

        for line in f:
            messages.append(line.strip())

    return (rules, messages)

def parse_rule_def(definition):
    if definition[0] == '"':
        return definition.strip('"')
    else:
        either = []
        conds = definition.split(' | ')
        for condition in conds:
            rules = condition.split(' ')
            either.append([int(rule) for rule in rules])
        return either


def part1(rules, messages):
    possible42 = get_all_possible_messages(rules, start_rule=42)
    possible31 = get_all_possible_messages(rules, start_rule=31)
    print("ALL POSSIBLE MESSAGES for 42")
    print('\n'.join(possible42))
    print("ALL POSSIBLE MESSAGES for 31")
    print('\n'.join(possible31))

    match_count = 0
    for message in messages:
        print("MESSAGE:", message)
        matches = True
        i = 0
        num42 = 0
        while i + 8 <= len(message):
            segment = message[i:i+8]
            if segment in possible42:
                i += 8
                num42 += 1
                print("segment", segment, "matches rule 42")
            else:
                print("segment", segment, "doesn't match rule 42, switching to rule 31")
                break

        num31 = 0
        while i + 8 <= len(message):
            segment = message[i:i+8]
            if segment in possible31:
                i += 8
                num31 += 1
                print("segment", segment, "matches rule 31")
            else:
                print("segment", segment, "doesn't match rule 31, message doesn't match")
                matches = False
                break

        print(i+8, len(message))

        if matches == True and num42 > num31 and num31 > 0:
            print("We found a match!")
            match_count += 1

    return match_count

eight_count = 0
eleven_count = 0

def get_all_possible_messages(rule_defs, start_rule=42):
    global eight_count
    global eleven_count

    if start_rule == 8:
        eight_count = eight_count + 1
        if eight_count >= 20:
            return get_all_possible_messages(rule_defs, start_rule=42)

    if start_rule == 11:
        eleven_count = eleven_count + 1
        if eleven_count >= 20:
            return rule_and([42, 31], rule_defs)

    print("Getting all possible messages for rule", str(start_rule))
    rule_def = rule_defs[start_rule]
    #print(start_rule, ':', rule_def)
    if type(rule_def) == str:
        #print("Base case:", rule_def)
        return rule_def
    elif type(rule_def) == list:
        if len(rule_def) == 1:
            return rule_and(rule_def[0], rule_defs)
        elif len(rule_def) == 2:
            return rule_or(rule_def, rule_defs)
        else:
            print('got a list that wasn\'t and/or', rule_def)
    else:
        print('Unknown rule type - rule:', rule_def)

def rule_and(rule_ids, rule_defs):
    #print("Getting all possibilities for", " ".join(str(rule_id) for rule_id in rule_ids))
    possibilities = ['']
    for rule_id in rule_ids:
        all_possible = get_all_possible_messages(rule_defs, start_rule=rule_id)
        print("Finished getting possible messages for", str(rule_id))

        # Combine possibilities
        new_p = []
        for p in possibilities:
            for q in all_possible:
                new_p.append(p + q)
        possibilities = new_p
    return set(possibilities)

def rule_or(rule_sets, rule_defs):
    #print("Getting all possibilities for", " | ".join(" ".join(str(rule) for rule in rule_set) for rule_set in rule_sets))
    possibilities = []
    for rule_set in rule_sets:
        possibilities += rule_and(rule_set, rule_defs)
    return set(possibilities)

def part2(processed):
    pass

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        (rules, messages) = preprocess(sys.argv[1])
        print(part1(rules, messages))
        #print(part2(processed))
