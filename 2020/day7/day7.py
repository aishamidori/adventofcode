import sys

allowed_containers = {}

def preprocess(file_path):
    with open(file_path) as f:
        for line in f:
            #print(line.strip())
            # Remove the period
            rules = line[:-1].split(' bags contain ')
            container = rules[0]

            print(rules[1])
            if rules[1] == 'no other bags.':
                continue

            # Should be in the form "<n> <color> bag(s), <m> <color> bag(s)"
            contained = rules[1].split(', ')
            for description in contained:
                #print(description)
                words = description[:description.find('bag') - 1].split(' ')
                count = words[0]
                color = ' '.join(words[1:])
                #print(count)
                #print(color)
                if container in allowed_containers:
                    allowed_containers[container].add((count, color))
                else:
                    allowed_containers[container] = {(count, color)}

    #added = set()
    #to_add = set(allowed_containers['shiny gold'])
    #allowed = set()
    #while to_add:
    #    (count, color) = to_add.pop()
    #    added.add(color)

    #    # Add all bags that can contain the container too
    #    if color in allowed_containers:
    #        new_colors = allowed_containers[color]
    #        for new_color in new_colors:
    #            if new_color not in added:
    #                to_add.add(new_color)
    print(count_bags_recursive('shiny gold') - 1)



def count_bags_recursive(color):
    print('Counting bags that have to be contained in a', color, 'bag')
    if not color in allowed_containers:
        return 1

    contained_bags = allowed_containers[color]
    print('A', color, 'bag contains', contained_bags)
    total_count = 0
    for (count, contained_color) in contained_bags:
        print(int(count), contained_color)
        total_count = total_count + (int(count) * count_bags_recursive(contained_color))
        print('New total:', total_count)
    return total_count + 1

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        preprocess(sys.argv[1])
