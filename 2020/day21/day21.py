from collections import defaultdict
from copy import copy, deepcopy
from functools import reduce
import sys

def preprocess(file_path):
    processed = []
    with open(file_path) as f:
        dishes = []
        for line in f:
            a = line.split('(contains ')
            allergens = a[-1][:-2].split(', ')
            ingredients = a[0][:-1].split(' ')
            dishes.append((ingredients, allergens))
    return dishes

def part1(processed):
    allergen_to_maybe_ingredient = {}
    allergen_to_ingredient = {}
    all_ingredient_counts = defaultdict(lambda: 0)
    for dish in processed:
        ingredients, allergens = dish
        #print("Dish:\n\tingredients -", ingredients, '\n\tallergens -', allergens)

        for ingredient in ingredients:
            all_ingredient_counts[ingredient] += 1

        for allergen in allergens:
            if not allergen in allergen_to_maybe_ingredient and not allergen in allergen_to_ingredient:
                maybe_allergen_set = set(ingredients)
                for ingredient in allergen_to_ingredient.values():
                    maybe_allergen_set.remove()
                allergen_to_maybe_ingredient[allergen] = maybe_allergen_set
                #print("Allergen", allergen, "could be in any of", maybe_allergen_set)
            else:
                new_maybe = allergen_to_maybe_ingredient[allergen].intersection(ingredients)
                allergen_to_maybe_ingredient[allergen] = new_maybe
                #print("Allergen", allergen, "could be in any of", new_maybe)
                if len(new_maybe) == 1:
                    # We only have one possible ingredient move it to the final dict
                    found_ingredient = list(new_maybe)[0]
                    allergen_to_ingredient[allergen] = found_ingredient
                    del allergen_to_maybe_ingredient[allergen]

                    # Each ingredient can only have 0 or 1 allergen
                    for ingredients in allergen_to_maybe_ingredient.values():
                        if found_ingredient in ingredients:
                            ingredients.remove(found_ingredient)

    non_allergen_count = 0
    allergen_ingredients = allergen_to_ingredient.values()
    maybe_allergen_ingredients = reduce(lambda a, b: a.union(b), allergen_to_maybe_ingredient.values())
    for ingredient, count in all_ingredient_counts.items():
        if not ingredient in allergen_ingredients and not ingredient in maybe_allergen_ingredients:
            #print("Ingredient", ingredient, "doesn't have any allergens and is present", count, "times.")
            non_allergen_count += count

    return non_allergen_count

def part2(processed):
    allergen_to_maybe_ingredient = {}
    allergen_to_ingredient = {}
    all_ingredient_counts = defaultdict(lambda: 0)
    for dish in processed:
        ingredients, allergens = dish
        #print("Dish:\n\tingredients -", ingredients, '\n\tallergens -', allergens)

        for ingredient in ingredients:
            all_ingredient_counts[ingredient] += 1

        for allergen in allergens:
            if not allergen in allergen_to_maybe_ingredient and not allergen in allergen_to_ingredient:
                maybe_allergen_set = set(ingredients)

                # Already allocated ingredients shouldn't be in the possible ingredients
                for ingredient in allergen_to_ingredient.values():
                    if ingredient in maybe_allergen_set:
                        maybe_allergen_set.remove(ingredient)
                allergen_to_maybe_ingredient[allergen] = maybe_allergen_set
                #print("Allergen", allergen, "could be in any of", maybe_allergen_set)
            else:
                new_maybe = allergen_to_maybe_ingredient[allergen].intersection(ingredients)
                allergen_to_maybe_ingredient[allergen] = new_maybe
                #print("Allergen", allergen, "could be in any of", new_maybe)
                if len(new_maybe) == 1:
                    # We only have one possible ingredient move it to the final dict
                    found_ingredient = list(new_maybe)[0]
                    allergen_to_ingredient[allergen] = found_ingredient
                    del allergen_to_maybe_ingredient[allergen]

                    # Each ingredient can only have 0 or 1 allergen
                    for ingredients in allergen_to_maybe_ingredient.values():
                        if found_ingredient in ingredients:
                            ingredients.remove(found_ingredient)

    i = 0
    while allergen_to_maybe_ingredient.keys():
        print("\nIteration %d:" % i)
        allergens = list(allergen_to_maybe_ingredient.keys())
        for allergen in allergens:
            maybe_set = allergen_to_maybe_ingredient[allergen]
            print(allergen, '\n\t', "\n\t".join(list(maybe_set)))
            if len(maybe_set) == 1:
                found_ingredient = list(maybe_set)[0]
                allergen_to_ingredient[allergen] = found_ingredient
                del allergen_to_maybe_ingredient[allergen]

                # Each ingredient can only have 0 or 1 allergen
                for ingredients in allergen_to_maybe_ingredient.values():
                    if found_ingredient in ingredients:
                        ingredients.remove(found_ingredient)

    print(allergen_to_ingredient)
    print(build_dangerous_ingredient_list(allergen_to_ingredient))

def build_dangerous_ingredient_list(allergen_to_ingredient):
    print(allergen_to_ingredient)
    allergens = list(allergen_to_ingredient.keys())
    allergens.sort()
    print(allergens)
    return ','.join([allergen_to_ingredient[allergen] for allergen in allergens])

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please provide a file argument")
    else:
        processed = preprocess(sys.argv[1])
        #print(part1(processed))
        print(part2(processed))
