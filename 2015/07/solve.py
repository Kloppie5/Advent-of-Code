from pathlib import Path
input_file = Path(__file__).parent / "input"

### Opcode emulation ###

def emulate_circuit_MOVwi ( circuit, target, imm, debug = False ) :
  if debug :
    print(f"MOVwi {target}, {imm}")
    print(f"  {target} = {imm}")
  circuit[target] = imm

def emulate_circuit_MOVww ( circuit, target, source, debug = False ) :
  if debug :
    print(f"MOVww {target}, {source}")
    print(f"  {target} = {circuit[source]}")
  circuit[target] = circuit[source]

def emulate_circuit_NOTi ( circuit, target, imm, debug = False ) :
  if debug :
    print(f"NOTi {target}, {imm}")
    print(f"  {target} = {~imm & 0xFFFF}")
  circuit[target] = ~imm & 0xFFFF

def emulate_circuit_NOTw ( circuit, target, source, debug = False ) :
  if debug :
    print(f"NOTwi {target}, {source}")
    print(f"  {target} = {~circuit[source] & 0xFFFF}")
  circuit[target] = ~circuit[source] & 0xFFFF

def emulate_circuit_ANDiw ( circuit, target, imm1, source2, debug = False ) :
  if debug :
    print(f"ANDiw {target}, {imm1}, {source2}")
    print(f"  {target} = {imm1 & circuit[source2]}")
  circuit[target] = imm1 & circuit[source2]

def emulate_circuit_ANDww ( circuit, target, source1, source2, debug = False ) :
  if debug :
    print(f"ANDww {target}, {source1}, {source2}")
    print(f"  {target} = {circuit[source1] & circuit[source2]}")
  circuit[target] = circuit[source1] & circuit[source2]

def emulate_circuit_ORwi ( circuit, target, source1, imm2, debug = False ) :
  if debug :
    print(f"ORwi {target}, {source1}, {imm2}")
    print(f"  {target} = {circuit[source1] | imm2}")
  circuit[target] = circuit[source1] | imm2

def emulate_circuit_ORww ( circuit, target, source1, source2, debug = False ) :
  if debug :
    print(f"ORww {target}, {source1}, {source2}")
    print(f"  {target} = {circuit[source1] | circuit[source2]}")
  circuit[target] = circuit[source1] | circuit[source2]

def emulate_circuit_LSHIFTwi ( circuit, target, source1, imm2, debug = False ) :
  if debug :
    print(f"LSHIFTwi {target}, {source1}, {imm2}")
    print(f"  {target} = {circuit[source1] << imm2}")
  circuit[target] = (circuit[source1] << imm2) & 0xFFFF

def emulate_circuit_RSHIFTwi ( circuit, target, source1, imm2, debug = False ) :
  if debug :
    print(f"RSHIFTwi {target}, {source1}, {imm2}")
    print(f"  {target} = {circuit[source1] >> imm2}")
  circuit[target] = circuit[source1] >> imm2

### Opcode selection ###

def emulate_circuit_op0 ( circuit, target, source, debug = False ) :
  source_is_imm = source.isdigit()
  source_imm = int(source) if source_is_imm else None

  if source_is_imm :
    emulate_circuit_MOVwi ( circuit, target, source_imm, debug )
  else:
    emulate_circuit_MOVww ( circuit, target, source, debug )

def emulate_circuit_op1 ( circuit, target, opcode, source, debug = False ) :
  source_is_imm = source.isdigit()
  source_imm = int(source) if source_is_imm else None

  if opcode == "NOT" :
    if source_is_imm :
      emulate_circuit_NOTi ( circuit, target, source_imm, debug )
    else:
      emulate_circuit_NOTw ( circuit, target, source, debug )
    return

  print(f"Unknown opcode: {opcode}")
  exit(1)

def emulate_circuit_op2 ( circuit, target, opcode, source1, source2, debug = False ) :
  source1_is_imm = source1.isdigit()
  source1_imm = int(source1) if source1_is_imm else None
  source2_is_imm = source2.isdigit()
  source2_imm = int(source2) if source2_is_imm else None

  if opcode == "OR" :
    if not source1_is_imm and not source2_is_imm :
      emulate_circuit_ORww ( circuit, target, source1, source2, debug )
      return

  if opcode == "AND" :
    if source1_is_imm and not source2_is_imm :
      emulate_circuit_ANDiw ( circuit, target, source1_imm, source2, debug )
      return
    if not source1_is_imm and not source2_is_imm :
      emulate_circuit_ANDww ( circuit, target, source1, source2, debug )
      return

  if opcode == "LSHIFT" :
    if not source1_is_imm and source2_is_imm :
      emulate_circuit_LSHIFTwi ( circuit, target, source1, source2_imm, debug )
      return

  if opcode == "RSHIFT" :
    if not source1_is_imm and source2_is_imm :
      emulate_circuit_RSHIFTwi ( circuit, target, source1, source2_imm, debug )
      return

  print(f"ERROR: Unknown opcode: {opcode}; {source1} {source2}")
  exit(1)

### Main ###

def emulate_circuit ( instructions, debug = False ) :
  circuit = {}

  if debug :
    print(f"Parsing instructions")
  operations = {}
  for instruction in instructions :
    operation = instruction.split(' -> ')[0]
    sc = operation.count(' ')
    target = instruction.split(' -> ')[1]

    if sc == 0 :
      source = operation
      operations[target] = {
        'func': emulate_circuit_op0,
        'args': [circuit, target, source, debug],
        'deps': [source]
      }
      continue

    if sc == 1 :
      opcode = operation.split(' ')[0]
      source = operation.split(' ')[1]
      operations[target] = {
        'func': emulate_circuit_op1,
        'args': [circuit, target, opcode, source, debug],
        'deps': [source]
      }
      continue

    if sc == 2 :
      source1 = operation.split(' ')[0]
      opcode = operation.split(' ')[1]
      source2 = operation.split(' ')[2]
      operations[target] = {
        'func': emulate_circuit_op2,
        'args': [circuit, target, opcode, source1, source2, debug],
        'deps': [source1, source2]
      }
      continue

    print(f"ERROR: {instruction}")

  if debug :
    print(f"Emulating circuit")
  targets = ['a']
  while len(targets) > 0 :
    target = targets[-1]
    if debug :
      print(f"Calculating {target}; {operations[target]['deps']}")
    deps = operations[target]['deps']
    for dep in deps :
      if dep.isdigit() :
        continue
      if dep not in circuit :
        if debug :
          print(f"  {dep} not in circuit")
        targets.append(dep)
    if target != targets[-1] :
      continue

    operations[target]['func'](*operations[target]['args'])
    targets.pop()

  if debug :
    print(f"Circuit: {circuit}")

  return circuit

if __name__ == "__main__":
  with open(input_file, "r") as f:
    instructions = [x.strip() for x in f.readlines()]
    circuit = emulate_circuit(instructions, True)
    print(f"Part 1: Wire a ends up with value {circuit['a']}")
