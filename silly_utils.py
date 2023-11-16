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

def label(sym, i=4):
    return "\n" + sym + ":"

def err(msg:str, errcode=1): # prints an err message and quits
    print("err: " + msg)
    sysexit(errcode)

def ext_env(env, ids, es):
    env = dict(env) # copy so as not to mut dict
    if type(ids) != list:
        ids = [ids]
    if type(es) != list:
        es = [es]
    l = min(len(es), len(ids))
    for i in range(l):
        env[ids[i]] = es[i]
    return env

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



