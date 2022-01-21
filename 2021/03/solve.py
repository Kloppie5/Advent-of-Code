from pathlib import Path
input_file = Path(__file__).parent / "input"

def parse_input ( input_file, debug = False ) :
  with open(input_file, "r") as f:
    data = f.read().splitlines()
  return data

def most_common_bit ( data, bit ) :
  return int(bit_ratio(data, bit) > 0.5)
def bit_ratio ( data, bit ) :
  return sum([ int(x[bit]) for x in data ]) / len(data)

def calculate_gamma_rate ( data ) :
  return ''.join([ str(most_common_bit(data, i)) for i in range(len(data[0])) ])

def calculate_epsilon_rate ( data ) :
  return ''.join([ str(1-most_common_bit(data, i)) for i in range(len(data[0])) ])

def calculate_oxygen_generator_rating ( data ) :
  for i in range(len(data[0])):
    ratio = bit_ratio(data, i)
    criteria_bit = str(int(ratio >= 0.5))
    data = [ x for x in data if x[i] == criteria_bit ]
    if len(data) == 1 :
      return data[0]

def calculate_co2_scrubber_rating ( data ) :
  for i in range(len(data[0])):
    ratio = bit_ratio(data, i)
    criteria_bit = str(int(ratio < 0.5))
    data = [ x for x in data if x[i] == criteria_bit ]
    if len(data) == 1 :
      return data[0]

if __name__ == "__main__":
  data = parse_input(input_file)
  gamma_rate = int(calculate_gamma_rate(data), 2)
  epsilon_rate = int(calculate_epsilon_rate(data), 2)
  oxygen_generator_rating = int(calculate_oxygen_generator_rating(data), 2)
  co2_scrubber_rating = int(calculate_co2_scrubber_rating(data), 2)
  print(f"Gamma rate: {gamma_rate}")
  print(f"Epsilon rate: {epsilon_rate}")
  print(f"Oxygen generator rating: {oxygen_generator_rating}")
  print(f"CO2 scrubber rating: {co2_scrubber_rating}")
  print(f"Part 1: {gamma_rate * epsilon_rate}")
  print(f"Part 2: {oxygen_generator_rating * co2_scrubber_rating}")
