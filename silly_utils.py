from sys import exit as sysexit

""" X86 INSTRUCTIONS (https://www.felixcloutier.com/x86/)"""
# registers
RAX = "rax"
RCX = "rcx"
RDX = "rdx"
RBX = "rbx"
RSP = "rsp"
RBP = "rbp"
RSI = "rsi"
RDI = "rdi"
R8  = "r8"
R9  = "r9"
R10 = "r10"
R11 = "r11"
R12 = "r12"
R13 = "r13"
R14 = "r14"
R15 = "r15"

# instructions
INC   = "inc"
DEC   = "dec"
ADD   = "add"
SUB   = "sub"
MUL   = "mul"
DIV   = "div"
CQO   = "cqo"
NOT   = "not"
AND   = "and"
OR    = "or"
XOR   = "xor"
CMP   = "cmp"
MOV   = "mov"
CMOVE = "cmove"
PUSH  = "push"
POP   = "pop"
LEA   = "lea"
CALL = "call"
RET = "ret"
JMP = "jmp"
JE  = "je"
JNE = "jne"
JG  = "jg"
JGE = "jge"
JL  = "jl"
JLE = "jle"
JZ  = "jz"
JNZ = "jnz"

global syms
syms = {}
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

# helper functions for running silly files

def lit_to_val(lit):
    return lit.v

def str_to_val(s):
    match s:
        case "true":
            return True
        case "false":
            return False
        case "unit":
            return None
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
        case None:
            return "unit"

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

# helper functions for writing inline asm

def offset(register, nbytes=0):
    return "[" + register + "+" + str(nbytes*8) + "]"

def label(sym, prefix="."):
    return prefix + sym

def flabel(sym):
    return label(sym)

def genlbl(*args, **kwargs):
    return label(gensym(*args), **kwargs)

def asm(lst:list, label="_entry", force_label=False) -> dict:
    ret = {label:[]}
    for l in lst:
        match l:
            case dict(l) | [dict(l)]: # [{label: [["mov", "rax", 11]]}]
                if force_label:
                    for _, code in l.items():
                        ret[label] += code
                else:
                    for llabel, code in l.items():
                        if not llabel in ret.keys():
                            ret[llabel] = []
                        ret[llabel] += code
            case list():
                first = list(ret.keys())[0]
                ret[label].append(l)
    return ret   

def _comment(c:str, prefix=" ", affix=""):
    if c != None:
        return f"{prefix}; {c}{affix}"
    else:
        return ""

def line_to_str(line:list, ind="", comment=None):
    if line[0][0] == "." or line[0][0] == "_":
        return f"{line[0]}:"
    return f"{ind}{line[0]} " + ", " .join(str(i) for i in line[1:]) + _comment(comment)

def text_to_str(asm:dict, ind:str="    ", comment=None):
    ret = f"section .text" + _comment(comment, prefix="\n")
    for label, code in (asm.items()):
        if label[0] == "_" or label[0] == ".":
            ret += f"\n\n{label}:\n"
            ret += f"\n".join(line_to_str(line, ind=ind) for line in code)
    return ret

def asm_prog_to_str(asm:dict, entry_label="_entry", type_label="_type", nasm_args=["default rel"], attrs=["EVAL_TYPE"]):
    assert entry_label in asm.keys()
    for attr in attrs:
        assert attr in asm.keys()
    if asm[entry_label][-1][0] != "ret":
        asm[entry_label].append(["ret"])
    nasm_args = "\n".join(nasm_args)
    type_val = asm["EVAL_TYPE"]
    return (

        f"[extern read_byte]\n"
        f"[extern peek_byte]\n"
        f"[extern write_byte]\n"
        
        f"global {entry_label}\n"
        f"global {type_label}\n"

        f"{nasm_args}\n\n"
        f"section .data\n"
        f"{type_label}: db {type_val}\n\n"
        f"{text_to_str(asm)}")

def write_prog_file(asm, path):
    with open(path, "w") as file:
        file.write(asm_prog_to_str(asm))

def pad_stack():
    return asm([
        [MOV, R15, RSP],
        [AND, R15, 0b1000],
        [SUB, RSP, R15]
    ])

def unpad_stack():
    return asm([
        [ADD, RSP, R15]
    ])

if __name__ == "__main__":

    s = asm(
        [["mov", "rax", 11]],
    )
    print(s)

    s = asm([
        ["mov", "rax", 11],
        ["ret"]
    ])
    print(s)

    s = asm([{
        "entry":[
            ["mov", "rax", 11],
            ["ret"]]}])
    print(s)

    testlbl = genlbl("test")
    s = asm([{
        "_entry":[
            ["mov", "rax", 11],
            ["jmp", testlbl],
            [testlbl],
            [testlbl],
            ["ret"]],
        "_subroutine":[
            ["pop", "rax"]
        ]}
    ])
    s["EVAL_TYPE"] = 1
    print(asm_prog_to_str(s))