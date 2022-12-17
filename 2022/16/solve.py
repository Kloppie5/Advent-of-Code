import sys
sys.stdout.reconfigure(encoding='utf-8')

def parse_input ( filename, debug = [] ) :
    if "functions" in debug :
        print(f"parse_input({filename})")
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        raw_data = f.read().splitlines()
    
    data = {}
    for i in range(len(raw_data)) :
        if "input" in debug :
            print(f"  > Input: {raw_data[i]}")
        # Valve __ has flow rate=_'tunnels lead to valves __
        line = raw_data[i].split("; tunnels lead to valves ")
        if len(line) == 1 : # "tunnel" case
            line = raw_data[i].split("; tunnel leads to valve ")
        line[0] = line[0].split(" has flow rate=")
        line[0][0] = line[0][0].split("Valve ")[1]
        line[1] = line[1].split(", ")
        data[line[0][0]] = {
            "flow" : int(line[0][1]),
            "tunnels" : line[1]
        }
        if "input" in debug :
            print(f"  < Parsed: {data[line[0][0]]}")
    return data

def minimize_paths ( data, useful_valves, debug = [] ) :
    if "functions" in debug :
        print(f"minimize_paths({data}, {useful_valves})")

    for valve in data :
        data[valve]["distances"] = {valve: 0}
    queue = [(valve, 0) for valve in useful_valves]
    while len(queue) > 0 :
        current, time = queue.pop(0)
        if "queue" in debug :
            print(f"  > Current({current}, {time})")
        for tunnel in data[current]["tunnels"] :
            for path in data[current]["distances"] :
                if path not in data[tunnel]["distances"] or data[tunnel]["distances"][path] > data[current]["distances"][path] + 1 :
                    data[tunnel]["distances"][path] = data[current]["distances"][path] + 1
                    if (tunnel, time+1) not in queue :
                        queue.append((tunnel, time+1))
                        if "queue" in debug :
                            print(f"      > Added to queue ({tunnel}, {time+1})")
        if "queue" in debug :
            print(f"  < Queue[{len(queue)}]: {queue}")
    
    data = {valve: data[valve] for valve in useful_valves}
    for valve in data :
        del data[valve]["tunnels"]
        data[valve]["distances"] = {path: data[valve]["distances"][path] for path in useful_valves if path != valve}

def iterate_all_valid_paths ( data, start, parallel_count, time_limit, debug = [] ) :
    if "functions" in debug :
        print(f"iterate_all_valid_paths({data}, {start}, {parallel_count}, {time_limit})")

    # ((valve, time),) -> {pressure -> [ ( [], ) ] }
    start = tuple([(start, 0) for i in range(parallel_count)])
    results = {}
    results[start] = {0: [[[] for i in range(parallel_count)]]}

    best_pressure = 0
    best_paths = [[[] for i in range(parallel_count)]]

    queue = [start]
    while len(queue) > 0 :
        spacetime = queue.pop(0)
        if "queue" in debug :
            print(f"  > Current({spacetime})")
        
        # For every different path that has led to this point in spacetime
        for pressure_release, paths in results[spacetime].items() :
            for path in paths :
                limit = True

                # For every possible addition to one of the traveller's paths
                for traveller in range(parallel_count) :
                    (position, time) = spacetime[traveller]
                    for room, distance in data[position]["distances"].items() :
                        if data[room]["flow"] == 0 :
                            continue
                        
                        # If the room is already in the path, skip it
                        for i in range(parallel_count) :
                            if room in path[i] :
                                break
                        else :

                            # Try to add it to the data and the queue
                            new_time = time + distance + 1
                            if new_time >= time_limit :
                                continue
                            new_spacetime = list(spacetime)
                            new_spacetime[traveller] = (room, new_time)
                            new_spacetime = tuple(new_spacetime)

                            if new_spacetime not in results :
                                results[new_spacetime] = {}
                            new_pressure_release = pressure_release + data[room]["flow"] * (time_limit - new_time)

                            if new_pressure_release not in results[new_spacetime] :
                                results[new_spacetime][new_pressure_release] = []
                            
                            new_path = [list(path[i]) for i in range(parallel_count)]
                            new_path[traveller] += [room]

                            if new_path not in results[new_spacetime][new_pressure_release] :
                                results[new_spacetime][new_pressure_release] += [new_path]
                                if new_spacetime not in queue :
                                    queue.append(new_spacetime)
                                    limit = False
                                    if "queue" in debug :
                                        print(f"      > Added to queue ({new_spacetime})")


                if limit :
                    if pressure_release > best_pressure :
                        best_pressure = pressure_release
                        best_paths = [path]
                    elif pressure_release == best_pressure :
                        best_paths += [path]

        queue.sort(key = lambda x: min(x[i][1] for i in range(parallel_count)))
        if "queue len" in debug :
            print(f"  < Queue[{len(queue)}]: {queue[-4:]}...")

    return results, best_pressure, best_paths

def divided_paths ( data, start, time_limit, debug = [] ) :
    # Separates the nodes over two paths and evaluates the pressure release
    results, _, _ = iterate_all_valid_paths(data, start, 1, time_limit, debug)
    group_bests = {}
    for spacetime, pressures in results.items() :
        for pressure, paths in pressures.items() :
            for path in paths :
                path[0].sort()
                path = frozenset(path[0])
                if path not in group_bests or group_bests[path] < pressure :
                    group_bests[path] = pressure
    group_bests = sorted(group_bests.items(), key = lambda x: x[1], reverse=True)

    best_pressure = 0
    best_paths = (None, None)
    for path_1, pressure_1 in group_bests :
        for path_2, pressure_2 in group_bests :
            if pressure_1 + pressure_2 > best_pressure and path_1.isdisjoint(path_2) :
                best_pressure = pressure_1 + pressure_2
                best_paths = (path_1, path_2)
    return best_pressure, best_paths

if __name__ == "__main__" :
    debug = ["queue len", "best"]

    data = parse_input("input")
    useful_valves = [x for x in data if data[x]["flow"] > 0] + ["AA"]
    minimize_paths(data, useful_valves)
    data = {valve: data[valve] for valve in useful_valves}
    
    results, best_pressure_1, best_paths_1 = iterate_all_valid_paths(data, "AA", 1, 30, debug)
    best_pressure_2, best_paths_2 = divided_paths(data, "AA", 26, debug)

    print(f"Part 1: best path {best_pressure_1} {best_paths_1}")
    print(f"Part 2: best path {best_pressure_2} {best_paths_2}")
