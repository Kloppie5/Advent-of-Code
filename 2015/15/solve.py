import copy

from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  data = {}
  with open(input_file, "r") as f:
    for line in f.read().splitlines() :
      line = line.split(':')
      ingredient = line[0]
      line = line[1].split(',')
      data[ingredient] = {}
      for x in line:
        prop, stat = x.strip().split()
        if stat != '0':
          data[ingredient][prop] = int(stat)
          if debug :
            print(f"{ingredient} : {prop} : {stat}")
  return data

def score ( recipe, data, debug = False ) :
  stats = {"capacity": 0, "durability": 0, "flavor": 0, "texture": 0, "calories": 0}
  for ingredient in recipe:
    amount = recipe[ingredient]
    if debug :
      print(f"{ingredient} : {amount}")
    for prop in data[ingredient]:
      stats[prop] += amount * data[ingredient][prop]
      if debug :
        print(f"{prop} : {stats[prop]}")
  for prop in stats:
    if stats[prop] < 0:
      stats[prop] = 0
  return stats["capacity"] * stats["durability"] * stats["flavor"] * stats["texture"]

def find_nd_feasible_recipes ( data, amount, debug = True ) :
  props = []
  for ingredient in data:
    for prop in data[ingredient]:
      if prop not in props:
        props.append(prop)
  if debug :
    print(f"Found properties: {props}")

  empty_recipe = {}
  for ingredient in data:
    empty_recipe[ingredient] = 0

  prev_recipes = [empty_recipe]
  if debug :
    print(f"Initial recipe: {prev_recipes}")

  for i in range(1, amount + 1):
    recipes = []

    # Build new recipes
    for recipe in prev_recipes:
      # Get recipe stats
      stats = {}
      for ingredient in data:
        for prop in data[ingredient]:
          if prop not in stats:
            stats[prop] = 0
          stats[prop] += recipe[ingredient] * data[ingredient][prop]

      # Fix first negative stat
      found = False
      for prop in props:
        if stats[prop] <= 0:
          for ingredient in data:
            if prop in data[ingredient] and data[ingredient][prop] > 0 :
              new_recipe = recipe.copy()
              new_recipe[ingredient] += 1
              if new_recipe not in recipes:
                recipes.append(new_recipe)
          found = True
          break

      # If no stat is negative, add all possible ingredients
      if not found:
        for ingredient in data:
          new_recipe = recipe.copy()
          new_recipe[ingredient] += 1
          if new_recipe not in recipes:
            recipes.append(new_recipe)

    prev_recipes = recipes
    if debug :
      print(f"{i}: {len(recipes)}")

  return prev_recipes

def bruteforce_solve ( data, amount, debug = False ) :
  recipes = find_nd_feasible_recipes(data, amount, debug)
  print(f"Found {len(recipes)} recipes")
  scores = []
  for recipe in recipes:
    scores.append(score(recipe, data))
  print(f"Max score: {max(scores)}")
  print(f"Recipe: {recipes[scores.index(max(scores))]}")

def decent_solve ( data, amount, debug = False ) :
  recipe = {}
  stats = {}
  for ingredient in data:
    recipe[ingredient] = 0
    for prop in data[ingredient]:
      if prop not in stats:
        stats[prop] = 0

  while sum(recipe.values()) < amount:
    found = None
    # Raise negative properties
    for prop in stats:
      if stats[prop] <= 0:
        for ingredient in data:
          if prop in data[ingredient] and data[ingredient][prop] > 0 :
            found = ingredient
    if debug and found is not None:
      print(f"Added {found} to fix property")

    if found is None:
      # Find ingredient with highest score
      max_score = 0
      for ingredient in data:
        i_stats = stats.copy()
        for prop in data[ingredient]:
          i_stats[prop] += data[ingredient][prop]
        i_score = i_stats["capacity"] * i_stats["durability"] * i_stats["flavor"] * i_stats["texture"]
        for prop in i_stats:
          if i_stats[prop] < 0:
            i_score = 0
            break
        if i_score > max_score:
          max_score = i_score
          found = ingredient
      if debug and found is not None:
        print(f"Added {found} to maximize score")

    if found is None:
      # No ingredient found, add one
      found = list(data.keys())[0]
      if debug :
        print(f"Added {found} to fix standstill")

    recipe[found] += 1
    for prop in data[found]:
      stats[prop] += data[found][prop]

    score = stats["capacity"] * stats["durability"] * stats["flavor"] * stats["texture"]
    for prop in stats:
      if stats[prop] < 0:
        score = 0
    if debug :
      print(f"Recipe: {recipe}")
      print(f"Stats: {stats}")
      print(f"Score: {score}")

  return recipe, stats, score

def proper_solve ( data, teaspoons, calorie_target, debug = False ) :
  if debug :
    print(f"proper_solve(\n  data = {data},\n  teaspoons = {teaspoons},\n  calorie_target = {calorie_target}\n)")

  # Scale everything based on the lowest calorie ingredient
  lowest_calorie = min([data[ingredient]["calories"] for ingredient in data])
  lowest_calorie_ingredient = None
  for ingredient in data :
    data[ingredient]["calories"] -= lowest_calorie
    if data[ingredient]["calories"] == 0:
      lowest_calorie_ingredient = ingredient

  recipe = {}
  stats = {}
  for ingredient in data:
    recipe[ingredient] = 0
    for prop in data[ingredient]:
      if prop not in stats:
          stats[prop] = 0

  recipe[lowest_calorie_ingredient] = teaspoons
  for prop in data[lowest_calorie_ingredient]:
    stats[prop] += data[lowest_calorie_ingredient][prop] * teaspoons
  del stats["calories"]
  minimum_calories = lowest_calorie * teaspoons

  ingredients = list(data.keys())
  ingredients.remove(lowest_calorie_ingredient)
  props = list(stats.keys())

  recipes = {}
  recipes[minimum_calories] = {"ingredients": recipe, "stats": stats}

  if debug :
    print(f"Starting recipes: {recipes}")

  for i in range(minimum_calories+1, calorie_target+1) :
    if debug :
      print(f"Trying to reach {i} calories")
    best_recipe = None
    least_worst_recipe = None
    best_score = 0
    least_worst_score = -100000
    for ingredient in ingredients :
      if i - data[ingredient]["calories"] in recipes :
        i_recipe = copy.deepcopy(recipes[i - data[ingredient]["calories"]])
        i_recipe["ingredients"][lowest_calorie_ingredient] -= 1
        i_recipe["ingredients"][ingredient] += 1
        for prop in props :
          if prop in data[lowest_calorie_ingredient] :
            i_recipe["stats"][prop] -= data[lowest_calorie_ingredient][prop]
          if prop in data[ingredient] :
            i_recipe["stats"][prop] += data[ingredient][prop]
        if debug :
          print(f"Found recipe: {i_recipe}")
        i_score = i_recipe["stats"]["capacity"] * i_recipe["stats"]["durability"] * i_recipe["stats"]["flavor"] * i_recipe["stats"]["texture"]
        least_worst_i_score = min([i_recipe["stats"][prop] for prop in props])
        for prop in props :
          if i_recipe["stats"][prop] < 0:
            i_score = 0
            break

        if i_score > best_score :
          best_recipe = i_recipe
          best_score = i_score

        if least_worst_i_score > least_worst_score :
          least_worst_recipe = i_recipe
          least_worst_score = least_worst_i_score

    if best_recipe is not None :
      if debug :
        print(f"Found best recipe: {best_recipe}")
      recipes[i] = best_recipe
    elif least_worst_recipe is not None :
      if debug :
        print(f"Found least worst recipe: {least_worst_recipe}")
      recipes[i] = least_worst_recipe

  return recipes[calorie_target]["ingredients"], recipes[calorie_target]["stats"], recipes[calorie_target]["stats"]["capacity"] * recipes[calorie_target]["stats"]["durability"] * recipes[calorie_target]["stats"]["flavor"] * recipes[calorie_target]["stats"]["texture"]

if __name__ == "__main__":
  data = parse_input(input_file)
  recipe, stats, score = decent_solve(data, 100)
  print(f"Part 1: {score}")
  recipe, stats, score = proper_solve(data, 100, 500)
  print(f"Part 2: {score}")
