import sys
sys.stdout.reconfigure(encoding='utf-8')
import math

class Tracker ( ) :
    from datetime import datetime

    def __init__ ( self, enabled = False ) :
        self.enabled = enabled
        self.data = {}
    def enable ( self ) :
        self.enabled = True
    def disable ( self ) :
        self.enabled = False
    
    def print ( self, tags, *args, **kwargs ) :
        # Todo; add tag filtering
        if not self.enabled : return
        print(*args, **kwargs)
    
    def print_all ( self ) :
        for key, value in self.data.items() :
            print(f"  {key}: {value}")

    def stat_inc ( self, key ) :
        if not self.enabled : return
        if key in self.data :
            self.data[key] += 1
        else :
            self.data[key] = 1

    def stat_max ( self, key, value ) :
        if not self.enabled : return
        if key in self.data :
            self.data[key] = max(self.data[key], value)
        else :
            self.data[key] = value

    def timer_start ( self, key ) :
        if not self.enabled : return
        time = self.datetime.now()
        self.data[key] = {"start": time, "stop": None, "total": None}
    
    def timer_stop ( self, key ) :
        if not self.enabled : return
        time = self.datetime.now()
        if key in self.data :
            self.data[key] = {"start": self.data[key]["start"], "stop": time, "total": time - self.data[key]["start"]}
        else :
            self.data[key] = {"start": None, "stop": time, "total": None}
    
    def timer_update ( self, key ) :
        if not self.enabled : return
        time = self.datetime.now()
        if key in self.data :
            self.data[key] = {"start": self.data[key]["start"], "stop": time, "total": time - self.data[key]["start"]}
        else :
            self.data[key] = {"start": time, "stop": None, "total": None}
tracker = Tracker()

# Solution attempt 1:
#  Basic queue, adding points one step in the future for all possible actions
#  Pruning based on complete coverage of inventory
# Solution attempt 2:
#  Replaced queue with sorted binary tree
#  Insertion kills off weaker nodes
#  Steps continue until the end or until it is possible to construct a bot
#   instead of stepping every minute
# Solution attempt 3:
#  Building construction path backwards based on minimal minutes between
#   construction of bots based on their costs using a triangular number lut
# Solution attempt 4:
#  Sorted queue, killing off weaker nodes
#  Early termination based on best possible geodes

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    # Blueprint _: Each ore robot costs _ ore. Each clay robot costs _ ore. Each obsidian robot costs _ ore and _ clay. Each geode robot costs _ ore and _ obsidian.
    for i in range(len(data)) :
        data[i] = data[i].split(" ")
        data[i] = (int(data[i][6]), int(data[i][12]), int(data[i][18]), int(data[i][21]), int(data[i][27]), int(data[i][30]))
    return data

def find_most_geodes ( blueprint, time_limit ) :
    tracker.timer_start(f"Runtime {blueprint}")
    ore_robot_cost, clay_robot_cost, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian = blueprint

    max_ore_cost = max(ore_robot_cost, clay_robot_cost, obsidian_robot_cost_ore, geode_robot_cost_ore)
    max_clay_cost = obsidian_robot_cost_clay
    max_obsidian_cost = geode_robot_cost_obsidian

    # (time, (ore_bots, clay_bots, obsidian_bots, geode_bots, ore, clay, obsidian, geodes))
    queue = [(0, (1, 0, 0, 0, 0, 0, 0, 0), [])]
    highest_geodes = 0

    def try_add_queue ( elem ) :
        overshadowed = False
        delete_queue = []
        for i in range(len(queue)) :
            if not overshadowed and queue[i][0] <= elem[0] and all(elem[1][j] <= queue[i][1][j] for j in range(8)) :
                overshadowed = True
            if elem[0] <= queue[i][0] and all(queue[i][1][j] <= elem[1][j] for j in range(8)) :
                delete_queue.append(i)
        for i in reversed(delete_queue) :
            del queue[i]
        if not overshadowed :
            queue.append(elem)
        queue.sort(key=lambda x: (x[0], x[1][7], x[1][6], x[1][5], x[1][4], x[1][3], x[1][2], x[1][1], x[1][0]), reverse=True)

    while len(queue) > 0 :
        time, inventory, history = queue.pop(0)
        tracker.timer_update(f"Runtime {blueprint}-{time}")

        ore_bots, clay_bots, obsidian_bots, geode_bots, ore, clay, obsidian, geodes = inventory
        
        time_left = time_limit - time
        potential_geodes = geodes + time_left * geode_bots + time_left * (time_left-1) // 2
        if potential_geodes < highest_geodes :
            tracker.print(["queue"], f"  > Potential Geodes ({potential_geodes}) < Highest Geodes ({highest_geodes})")
            continue

        if ore_bots < max_ore_cost :
            time_until_ore_bot = max(0, math.ceil((ore_robot_cost - ore) / ore_bots)) + 1
            if time + time_until_ore_bot < time_limit :
                make_ore_bot = (time+time_until_ore_bot, (ore_bots+1, clay_bots, obsidian_bots, geode_bots, ore-ore_robot_cost+time_until_ore_bot*ore_bots, clay+time_until_ore_bot*clay_bots, obsidian+time_until_ore_bot*obsidian_bots, geodes+time_until_ore_bot*geode_bots), history+[(time+time_until_ore_bot, "ore_bot")])
                tracker.print(["queue"], f"  > Make Ore Bot: {make_ore_bot}")
                try_add_queue(make_ore_bot)
        
        if clay_bots < max_clay_cost :
            time_until_clay_bot = max(0, math.ceil((clay_robot_cost - ore) / ore_bots)) + 1
            if time + time_until_clay_bot < time_limit :
                make_clay_bot = (time+time_until_clay_bot, (ore_bots, clay_bots+1, obsidian_bots, geode_bots, ore-clay_robot_cost+time_until_clay_bot*ore_bots, clay+time_until_clay_bot*clay_bots, obsidian+time_until_clay_bot*obsidian_bots, geodes+time_until_clay_bot*geode_bots), history+[(time+time_until_clay_bot, "clay_bot")])
                tracker.print(["queue"], f"  > Make Clay Bot: {make_clay_bot}")
                try_add_queue(make_clay_bot)
        
        if clay_bots > 0 and obsidian_bots < max_obsidian_cost :
            time_until_obsidian_bot = max(0, math.ceil((obsidian_robot_cost_ore - ore) / ore_bots), math.ceil((obsidian_robot_cost_clay - clay) / clay_bots)) + 1
            if time + time_until_obsidian_bot < time_limit :
                make_obsidian_bot = (time+time_until_obsidian_bot, (ore_bots, clay_bots, obsidian_bots+1, geode_bots, ore-obsidian_robot_cost_ore+time_until_obsidian_bot*ore_bots, clay-obsidian_robot_cost_clay+time_until_obsidian_bot*clay_bots, obsidian+time_until_obsidian_bot*obsidian_bots, geodes+time_until_obsidian_bot*geode_bots), history+[(time+time_until_obsidian_bot, "obsidian_bot")])
                tracker.print(["queue"], f"  > Make Obsidian Bot: {make_obsidian_bot}")
                try_add_queue(make_obsidian_bot)
        
        if obsidian_bots > 0 :
            time_until_geode_bot = max(0, math.ceil((geode_robot_cost_ore - ore) / ore_bots), math.ceil((geode_robot_cost_obsidian - obsidian) / obsidian_bots)) + 1
            if time + time_until_geode_bot < time_limit :
                make_geode_bot = (time+time_until_geode_bot, (ore_bots, clay_bots, obsidian_bots, geode_bots+1, ore-geode_robot_cost_ore+time_until_geode_bot*ore_bots, clay+time_until_geode_bot*clay_bots, obsidian-geode_robot_cost_obsidian+time_until_geode_bot*obsidian_bots, geodes+time_until_geode_bot*geode_bots), history+[(time+time_until_geode_bot, "geode_bot")])
                tracker.print(["queue"], f"  > Make Geode Bot: {make_geode_bot}")
                try_add_queue(make_geode_bot)
        
        if geode_bots > 0 :
            final_geodes = geodes + time_left*geode_bots
            if final_geodes > highest_geodes :
                tracker.print(["queue"], f"  > New Highest Geodes: {final_geodes}")
                highest_geodes = final_geodes
        
        tracker.print(["queue"], f"  < Queue[{len(queue)}]: {queue[:4]}")
        tracker.stat_max("Max Queue Length", len(queue))

    tracker.timer_stop(f"Runtime {blueprint}")
    return highest_geodes

if __name__ == "__main__" :
    # tracker.enable()

    test_1 = find_most_geodes((4, 2, 3, 14, 2, 7), 24)
    if test_1 != 9 :
        raise Exception(f"Test 1 failed; got {test_1}, expected 9")
    test_2 = find_most_geodes((2, 3, 3, 8, 3, 12), 24)
    if test_2 != 12 :
        raise Exception(f"Test 2 failed; got {test_2}, expected 12")

    blueprints = parse_input("input")

    total_quality = 0
    for i, blueprint in enumerate(blueprints) :
        highest_geodes = find_most_geodes(blueprint, 24)
        quality_level = (i+1)*highest_geodes
        total_quality += quality_level
        print(f"Blueprint {i+1}: {highest_geodes} geodes, quality level {quality_level}")
    
    print(f"Total Quality: {total_quality}")
