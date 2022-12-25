import sys
sys.stdout.reconfigure(encoding='utf-8')

import math

def parse_input ( filename ) :
    from pathlib import Path
    with open(Path(__file__).parent / filename, "r") as f :
        data = f.read().splitlines()
    
    return data

def snafu_to_dec ( numbers ) :
    result = []
    snafu_to_dec_lut = "=-012"
    for snafu in numbers :
        number = 0
        for char in snafu :
            number *= 5
            number += snafu_to_dec_lut.index(char) - 2
        result.append(number)
    
    return result

def snafu_add ( numbers ) :
    total = []
    snafu_to_dec_lut = "=-012"
    for snafu in numbers :
        i = 0
        for char in snafu[::-1] :
            if i == len(total) :
                total.append(0)
            total[i] += snafu_to_dec_lut.index(char) - 2
            i += 1
    
    for i in range(len(total)) :
        if i == len(total) - 1 :
            total.append(0)
        while total[i] < -2 :
            total[i] += 5
            total[i + 1] -= 1
        while total[i] > 2 :
            total[i] -= 5
            total[i + 1] += 1
    
    result = ""
    for i in range(len(total)) :
        result = snafu_to_dec_lut[total[i] + 2] + result
    while result[0] == "0" :
        result = result[1:]
  
    return result

if __name__ == "__main__" :
    data = parse_input("input")

    part_1 = snafu_add(data)
    print(f"Part 1: {part_1}")
    