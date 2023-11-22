from sys import exit as sysexit
global syms
syms = {}

x86ref = "https://www.felixcloutier.com/x86/"

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
    return name + str(num)

def err(msg:str, errcode=1): # prints an err message and quits
    print("err: " + msg)
    sysexit(errcode)

def lit_to_val(lit):
    return lit.v

def str_to_val(s):
    match s:
        case "true":
            return True
        case "false":
            return False
        case _:
            return int(s)

def lit_to_str(lit) -> str:
    match lit.v:
        case True:
            return "true"
        case False:
            return "false"
        case int():
            return str(lit.v)

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

