from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( debug = False ) :
    with open(input_file, "r") as f :
        data = f.read().splitlines()
    return data

def print_file_system ( file_system ) :
    def print_dir ( dir, depth ) :
        for entry in dir :
            if entry == "type" or entry == "size" :
                continue
            if dir[entry]["type"] == "dir" :
                if "size" in dir[entry] :
                    print(f"{'  ' * depth}- {entry} (dir, size={dir[entry]['size']})")
                else :
                    print(f"{'  ' * depth}- {entry} (dir)")
                print_dir(dir[entry], depth + 1)
            else :
                print(f"{'  ' * depth}- {entry} (file, size={dir[entry]['size']})")
    print_dir(file_system["/"], 0)

def process_command_line ( file_system, command_line, debug = False ) :
    command = command_line.pop(0)
    if command[0] != "$" :
        print(f"CRITICAL: Command {command} does not start with $")
        exit(1)
    command = command.split(' ')[1:]

    if command[0] == "cd" :
        if len(command) != 2 :
            print(f"CRITICAL: cd command must have exactly one argument")
            exit(1)
        target = command[1]
        if debug :
            print(f"> cd: {target}")
        if target == "/" :
            file_system["current_dir"] = ["/"]
        elif target == ".." :
            file_system["current_dir"].pop()
        else :
            file_system["current_dir"].append(target)

    elif command[0] == "ls" :
        if len(command) != 1 :
            print(f"CRITICAL: ls command must have no arguments")
            exit(1)
        current_dir = file_system
        for dir in file_system["current_dir"] :
            current_dir = current_dir[dir]
        if debug :
            print(f"> ls: {file_system['current_dir']}")
        
        while len(command_line) > 0 and command_line[0][0] != "$" :
            entry = command_line.pop(0)
            size_or_type, name = entry.split(' ')
            if size_or_type == "dir" :
                current_dir[name] = {
                    "type" : "dir"
                }
                if debug :
                    print(f"  Added directory {name}")
            else :
                current_dir[name] = {
                    "type" : "file",
                    "size" : size_or_type
                }
                if debug :
                    print(f"  Added file {name} with size {size_or_type}")
    
    return file_system, command_line

def calculate_dir_sizes ( file_system, debug = False ) :
    def calculate_dir_size ( dir ) :
        size = 0
        for entry in dir :
            if entry == "type" or entry == "size" :
                continue
            if dir[entry]["type"] == "dir" :
                size += calculate_dir_size(dir[entry])
            else :
                size += int(dir[entry]["size"])
        dir["size"] = size
        return size
    return calculate_dir_size(file_system["/"])

def all_dirs ( file_system ) :
    dirs = []
    def find_dirs ( dir ) :
        for entry in dir :
            if entry == "type" or entry == "size" :
                continue
            if dir[entry]["type"] == "dir" :
                dirs.append(dir[entry])
                find_dirs(dir[entry])
    find_dirs(file_system)
    return dirs

def sort_dirs ( file_system ) :
    dirs = all_dirs(file_system)
    dirs.sort(key = lambda dir : dir["size"])
    return dirs

if __name__ == "__main__":
    file_system = {
        "/" : { "type" : "dir" },
        "current_dir" : ["/"]
    }

    data = parse_input()

    while len(data) > 0 :
        file_system, data = process_command_line(file_system, data)
    
    calculate_dir_sizes(file_system)
    print_file_system(file_system)

    sorted_dirs = sort_dirs(file_system["/"])
    small_dirs = [dir for dir in sorted_dirs if dir["size"] < 100000]
    print(f"Found {len(small_dirs)} small directories")

    total_size = 0
    for small_dir in small_dirs :
        total_size += small_dir["size"]
    print(f"Total size of small directories: {total_size}")

    used_disk_space = file_system["/"]["size"]
    required_free_space = used_disk_space - 40000000
    print(f"Used disk space: {used_disk_space}")
    print(f"Required free space: {required_free_space}")
    # first dir that is big enough
    smallest_dir = [dir for dir in sorted_dirs if dir["size"] >= required_free_space][0]
    print(f"Size of smallest dir that is big enough: {smallest_dir['size']}")
