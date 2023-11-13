def err(msg:str):
    print("err: " + msg)
    quit()


def asm(*args:tuple[tuple|str], ind="    ") -> str:
    s = ""
    for instr in args:
        if type(instr) == tuple:
            s += "\n" + ind + instr[0] + " " + instr[1]
            for sym in instr[2:]:
                s += ", " + str(sym) 
        else:
            s += "\n" + instr
    return s