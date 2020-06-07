import sys
program = []
opcodes_list = []
with open(sys.argv[1],"rb") as f:
    p = []
    p = f.read()
    for i in p: program.append(hex(i))

def order(input):
    h = input.replace("0x","")
    if len(h)==1: h = "0"+h
    return h

# -----------SCRIBE FUNCTIONS-----------
def zeros():
    if op[2] == "e":
        if op[3] == "0": return "CLS"
        elif op[3] == "e": return "RET"

    elif "0000" in op:return "SYS"
    else: return "LOAD"+" "+op[1:4]

def jump():return "JUMP "+op[1:4]

def subroutine(): return "CALL "+op[1:4]

def three_skip(): return "SKIPIF V"+op[1]+" == "+op[2:4]#first is the register

def four_skip(): return "SKIPIF V"+op[1]+" != "+op[2:4]

def five_skip(): return "SKIPIF V"+op[1]+" == V"+op[2]#	Skips the next instruction if VX equals VY.

def set(): return "SET V"+op[1]+" "+op[2:4]

def add(): return "V"+op[1]+" += "+op[2:4]

def eight_values():
    if op[3] == "0":return "V"+op[1]+" = V"+op[2]
    elif op[3] == "1":return "V"+op[1]+"= V"+op[1]+" | "+op[2]
    elif op[3] == "2":return "V"+op[1]+"= V"+op[1]+" & "+op[2]
    elif op[3] == "3":return "V"+op[1]+"= V"+op[1]+" XOR "+op[2]
    elif op[3] == "4":return "V"+op[1]+" += V"+op[2]#Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't.
    elif op[3] == "5":return "V"+op[1]+" -= V"+op[2]
    elif op[3] == "6":return "V"+op[1]+" >>= 1"#Stores the least significant bit of VX in VF and then shifts VX to the right by 1
    elif op[3] == "7":return "V"+op[1]+" = V"+op[2]+" - "+op[1]
    elif op[3] == "e":return "V"+op[1]+" <<= 1"
    else: return "COMMAND NOT RECOGNISED"

def nine_jump():return "SKIPIF V"+op[1]+" != V"+op[2]

def set_addr(): return "IMEM = "+op[1:4]

def jump_plus(): return "JUMP "+op[1:4]+" +V0"

def rand(): return "V"+op[1]+" = RAND & "+op[2:4]

def draw():return "DRAW X"+op[1]+" Y"+op[2]+" H"+op[3]#Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels. Each row of 8 pixels is read as bit-coded starting from memory location I; I value doesn’t change after the execution of this instruction. As described above, VF is set to 1 if any screen pixels are flipped from set to unset when the sprite is drawn, and to 0 if that doesn’t happen

def e_skips():
    if op[2:4] == "9e":return "SKIPIF V"+op[1]+" PRESS"
    elif op[2:4] == "a1":return "SKIPIF V"+op[1]+"NOT PRESS"
    else:return "COMMAND NOT RECOGNISED"

def f_control():
    if op[2:4] == "07":return "V"+op[1]+" = DELTIME"
    elif op[2:4] == "0a":return "HALT V"+op[1]+" = KEY"
    elif op[2:4] == "15":return "DELTIME = V"+op[1]
    elif op[2:4] == "18":return "SOUNDTIME = V"+op[1]
    elif op[2:4] == "1e":return "IMEM += V"+op[1]
    elif op[2:4] == "29":return "IMEM = V"+op[1]+" CHARLOC"
    elif op[2:4] == "33":return "IMEM = BCD V"+op[1]
    elif op[2:4] == "55":return "MEM IMEM = V0-V"+op[1]
    elif op[2:4] == "65":"V0-V"+op[1]+" MEM IMEM"
    else:return "COMMAND NOT RECOGNISED"
#---------------------------------------
for i in range(0,len(program),2):
    opcodes_list.append(order(program[i])+order(program[i+1]))

first_nibble_functions = {# # marks if it will be an intersection
                        "0":zeros,
                        "1":jump,#
                        "2":subroutine,#
                        "3":three_skip,#
                        "4":four_skip,#
                        "5":five_skip,#
                        "6":set,#
                        "7":add,#
                        "8":eight_values,
                        "9":nine_jump,#
                        "a":set_addr,#
                        "b":jump_plus,#
                        "c":rand,#
                        "d":draw,#
                        "e":e_skips,
                        "f":f_control}
for op in opcodes_list:
    print(op+"  ",first_nibble_functions[op[0]]())
