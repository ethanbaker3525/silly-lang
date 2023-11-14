from sys import exit as sysexit
global syms
syms = {}

x86ref = "https://www.felixcloutier.com/x86/"

types = {
    "num"  : 0,
    "int"  : 0,
    "bool" : 1,
    "char" : 2,
    "str"  : 2
}

def gensym(*args, syms=syms): # generates a unique string for use in asm labels
    if len(args) > 0:
        name = args[0]
    else:
        name = "sym"
    if name in syms.keys():
        num = syms[name]
        syms[name] = num + 1
    else:
        num = 0
        syms[name] = 1
    return "." + name + str(num)

def label(sym, i=4):
    return "\n" + sym + ":"

def err(msg:str, errcode=1): # prints an err message and quits
    print("err: " + msg)
    sysexit(errcode)


def asm(*args:tuple[tuple|str], i:int=4, c:str=None) -> str:
    s = "\n" + (" " * i) +"; " + c if c != None else ""
    for instr in args:
        if type(instr) == tuple:
            s += "\n" + (" " * i) + instr[0] + " " + instr[1]
            for sym in instr[2:]:
                s += ", " + str(sym) 
        else:
            s += "\n" + instr.strip("\n")
    return s

def val_to_bits(v):
    if type(v) == int:
        return v
    elif type(v) == bool:
        if v: 
            return 1
        return 0
    elif type(v) == str:
        assert len(v) == 1
        return ord(v[0])

def get_type_str(tn0:int) -> str:
    for ts, tn1 in types.items():
        if tn0 == tn1:
            return ts