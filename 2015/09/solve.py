from pathlib import Path
input_file = Path(__file__).parent / "input"

from itertools import permutations

def all_routes ( distances, debug = False ) :
  cities = list(distances.keys())
  routes = {}
  for route in permutations(cities) :
    if debug :
      print(f"Route: {route}")
    route_length = 0
    for i in range(len(route)-1) :
      route_length += distances[route[i]][route[i+1]]
    if debug :
      print(f"Route length: {route_length}")
    routes[route] = route_length
  return routes

if __name__ == "__main__":
  distances = {}
  with open(input_file, "r") as f:
    for line in f:
      line = line.strip()
      line, distance = line.split(' = ')
      source, target = line.split(' to ')
      distances[source] = distances.get(source, {})
      distances[source][target] = int(distance)
      distances[target] = distances.get(target, {})
      distances[target][source] = int(distance)

  routes = all_routes(distances)
  print(f"Part 1: Shortest route: {min(routes.values())}")
  print(f"Part 2: Longest route: {max(routes.values())}")
