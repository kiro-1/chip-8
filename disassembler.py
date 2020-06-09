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

    elif "0000" in op:return "SYS "+op[1:4]
    else: return "COMMAND NOT RECOGNISED"

def jump():return "JP "+op[1:4]

def subroutine(): return "CALL "+op[1:4]

def three_skip(): return "SE "+op[1]+" == "+op[2:4]

def four_skip(): return "SNE "+op[1]+" != "+op[2:4]

def five_skip(): return "SE "+op[1]+" == "+op[2]

def set(): return "LD "+op[1]+" "+op[2:4]

def add(): return "ADD "+op[1]+" += "+op[2:4]

def eight_values():
    f = {"0":"LD "+op[1]+" = "+op[2],
    "1":op[1]+" = "+op[1]+" OR "+op[2],
    "2":op[1]+" = "+op[1]+" AND "+op[2],
    "3":op[1]+" = "+op[1]+" XOR "+op[2],
    "4":"ADD "+op[1]+" "+op[2],
    "5":"SUB "+op[1]+" "+op[2],
    "6":"SHR "+op[1]+"{, "+op[2]+"}",
    "7":"SUBN "+op[1]+" "+op[2],
    "e":"SHL "+op[1]+"{, "+op[2]+"}"}
    try: return f[op[3]]
    except: return "COMMAND NOT RECOGNISED"

def nine_jump():return "SNE"+op[1]+" "+op[2]

def set_addr(): return "LD I "+op[1:4]

def jump_plus(): return "JP "+"V0 "+op[1:4]

def rand(): return "RND "+op[1]+" "+op[2:4]

def draw():return "DRW "+op[1]+" "+op[2]+" "+op[3]

def e_skips():
    return "SKP "+op[1] if op[2:4] == "9e" else "SKNP "+op[1] if op[2:4]=="a1" else "COMMAND NOT RECOGNISED"

def f_control():
    f = {"07":"LD "+op[1]+", DT",
    "0a":"LD "+op[1]+", K",
    "15":"LD DT, "+op[1],
    "18":"LD ST, "+op[1],
    "1e":"ADD I, "+op[1],
    "29":"LD F, "+op[1],
    "33":"LD B, "+op[1],
    "55":"LD [I], "+op[1],
    "65":"LD "+op[1]+", [I]",}
    try: return f[op[2:4]]
    except:
        return "COMMAND NOT RECOGNISED"

#---------------------------------------
for i in range(0,len(program),2):
    opcodes_list.append(order(program[i])+order(program[i+1]))

first_nibble_functions = {# # marks if it will be an intersection, a dictionary emulating a switch case
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
