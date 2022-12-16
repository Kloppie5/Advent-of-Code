import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename, debug = False ) :
    if debug :
        print(f"parse_input({filename})")
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    for i in range(len(data)) :
        if debug :
            print(f"  > Input: {data[i]}")
        # Valve __ has flow rate=_'tunnels lead to valves __
        line = data[i].split("; tunnels lead to valves ")
        if len(line) == 1 : # "tunnel" case
            line = data[i].split("; tunnel leads to valve ")
        line[0] = line[0].split(" has flow rate=")
        line[0][0] = line[0][0].split("Valve ")[1]
        line[1] = line[1].split(", ")
        data[i] = {
            "valve" : line[0][0],
            "flow" : int(line[0][1]),
            "tunnels" : line[1]
        }
        if debug :
            print(f"  < Parsed: {data[i]}")
    data = {x["valve"] : x for x in data}
    return data

def minimize_paths ( data, useful_valves, debug = [] ) :
    if "functions" in debug :
        print(f"minimize_paths({data}, {useful_valves})")

    distances = {valve: {valve: 0} for valve in data}
    queue = [(valve, 0) for valve in useful_valves]
    while len(queue) > 0 :
        current, time = queue.pop(0)
        if "queue" in debug :
            print(f"  > Current({current}, {time})")
        for tunnel in data[current]["tunnels"] :
            for path in distances[current] :
                if path not in distances[tunnel] or distances[tunnel][path] > distances[current][path] + 1 :
                    distances[tunnel][path] = distances[current][path] + 1
                    if (tunnel, time+1) not in queue :
                        queue.append((tunnel, time+1))
                        if "queue" in debug :
                            print(f"      > Added to queue ({tunnel}, {time+1})")
        if "queue" in debug :
            print(f"  < Queue[{len(queue)}]: {queue}")
    for useful_valve in useful_valves :
        data[useful_valve]["distances"] = {path: distances[useful_valve][path] for path in useful_valves if path != useful_valve}

def iterate_all_valid_paths ( data, start, time_limit, debug = [] ) :
    if "functions" in debug :
        print(f"iterate_all_valid_paths({data}, {time_limit})")

    results = {valve: {} for valve in data}
    results[start][0] = {0 : [[]]}
    best_path = (0, [])
    queue = [(start, 0)]
    while len(queue) > 0 :
        current, time = queue.pop(0)
        if "queue" in debug :
            print(f"  > Current({current}, {time})")
        for pressure_release, paths in results[current][time].items() :
            for path in paths :
                limit = True
                for tunnel, distance in data[current]["distances"].items() :
                    if tunnel in path :
                        continue
                    new_time = time + distance + 1
                    if new_time >= time_limit :
                        continue
                    if new_time not in results[tunnel] :
                        results[tunnel][new_time] = {}
                    new_pressure_release = pressure_release + data[tunnel]["flow"] * (time_limit - new_time)
                    if new_pressure_release not in results[tunnel][new_time] :
                        results[tunnel][new_time][new_pressure_release] = []
                    if path + [tunnel] not in results[tunnel][new_time][new_pressure_release] :
                        results[tunnel][new_time][new_pressure_release] += [path + [tunnel]]
                        if (tunnel, new_time) not in queue :
                            queue.append((tunnel, new_time))
                            limit = False
                            if "queue" in debug :
                                print(f"      > Added to queue ({tunnel}, {new_time})")
                if limit and pressure_release > best_path[0] :
                    if "best" in debug :
                        print(f"      > New best path ({pressure_release}): {path}")
                    best_path = (pressure_release, path)
        queue.sort(key = lambda x: x[1])
        if "queue" in debug :
            print(f"  < Queue[{len(queue)}]: {queue}")
    return results, best_path

if __name__ == "__main__" :
    data = parse_input("input")
    useful_valves = [x for x in data if data[x]["flow"] > 0] + ["AA"]
    minimize_paths(data, useful_valves)
    data = {valve: data[valve] for valve in useful_valves}
    
    for valve in data :
        print(f"{valve}: {data[valve]['flow']} {data[valve]['distances']}")

    paths, best_path = iterate_all_valid_paths(data, "AA", 30, ["queue", "best"])
    print(f"Best path: {best_path}")

    
