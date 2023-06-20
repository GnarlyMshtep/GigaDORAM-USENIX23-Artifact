"""
Bristol Fashion:
Gates Wires
Inputs Bits_1 ... Bits_Inputs
Outputs Bits_1 ...

Inputs Outputs Wire1 Wire2 [Wire3] Type
...

circuit input format (1 block)
x1 | x2 | y

output format (1 block)
let found = (x1 == x2) in
x if found | y if found | found | 31b unused 
"""

num_wire_used = 0
gates = []

def make_block(width):
    global num_wire_used
    num_wire_used += width
    return (num_wire_used - width, num_wire_used)

def merge(b1, b2):
    b1_start, b1_end = b1
    b2_start, b2_end = b2
    assert(b1_end == b2_start)
    return (b1_start, b2_end)

def width_of(b):
    return b[1] - b[0]

def one_input_gate(b1, gate_type):
    assert gate_type in ("INV","EQW")
    b1_start, b1_end = b1
    width = width_of(b1)
    b2 = make_block(width)
    b2_start, b2_end = b2
    for i in range(width):
        gates.append([1,1,b1_start+i, b2_start+i, gate_type])
    return b2
        
def two_input_gate(b1, b2, gate_type):
    assert gate_type in ("XOR",)
    b1_start, b1_end = b1
    b2_start, b2_end = b2
    width = width_of(b1)
    assert width_of(b2) == width
    b3 = make_block(width)
    b3_start, b3_end = b3
    for i in range(width):
        gates.append([2,1,b1_start+i, b2_start+i, b3_start+i, gate_type])
    return b3

def multi_gate(b1, b2, gate_type):
    assert gate_type in ("MAND",)
    width = width_of(b1)
    b3 = make_block(width)
    if width_of(b2) == width:
        gates.append([2 * width, width] + list(range(*b1)) + list(range(*b2)) + list(range(*b3)) + [gate_type]);
    elif width_of(b2) == 1:
        b2_wire, _ = b2
        gates.append([2 * width, width] + list(range(*b1)) + [b2_wire] * width + list(range(*b3)) + [gate_type]);
    else:
        raise ValueError(f"{width_of(b2)} != {width_of(b1)} or 1")
    return b3


def inv_gate(b1):
    return one_input_gate(b1, "INV")

def eqw_gate(b1):
    return one_input_gate(b1, "EQW")

def xor_gate(b1, b2):
    return two_input_gate(b1, b2, "XOR")

def mand_gate(b1, b2):
    return multi_gate(b1, b2, "MAND")

def and_all(b):
    start, end = b
    width = width_of(b)
    if width == 1:
        return b
    mid = (start + end) // 2 
    left = (start, mid)
    right = (mid, end)
    left_and_right = mand_gate(left, right)
    return and_all(left_and_right)

def equal(b1, b2):
    return and_all(inv_gate(xor_gate(b1,b2)))

# by using variables, topsort order is enforced!        
x1 = make_block(32)
x2 = make_block(32)
y = make_block(64)
xs_equal = equal(x1, x2)
output = mand_gate(merge(x2, y), xs_equal)
found = eqw_gate(xs_equal)
output_unused = make_block(31)

print(len(gates), num_wire_used)
print(1, 128)
print(1, 128)
print("")
for gate in gates:
    print(" ".join(map(str, gate)))
