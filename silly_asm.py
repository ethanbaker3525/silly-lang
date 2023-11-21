from silly_types import get_type_str

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

# simple instructions
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

# label instructions
LBL = ":"
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

class Asm:

    TEMPLATE = (
    "global {s}\n"
    "global {t}\n"
    "{nasm_args}\n"

    "\nsection .data\n"
    "{t}: db {tn} ; eval type is {ts}\n"

    "\nsection .text\n"
    "{s}:\n{asm}"
        "ret"
    )

    @staticmethod
    def concat_instrs(instrs, ind=4, end="\n"):
        s = " " * ind
        #print(instrs)
        if instrs[0] == LBL:
            s = "." + instrs[1] + LBL
        elif instrs[0] in [RET]:
            s + instrs[0]
        elif instrs[0] in [JMP, JE, JNE, JG, JGE, JL, JLE, JZ, JNZ]:
            s += instrs[0] + " ." + instrs[1]
        else:
            s += instrs[0] + " " + ", ".join(instrs[1:])
        return s + end

    def __init__(self, code:list, eval_type:int=-1, eval_type_str:str=None):
        self.eval_type = eval_type
        self.eval_type_str = eval_type_str
        self.asm = []
        for data in code:
            if type(data) == Asm:
                    self.asm += data.asm
            elif type(data) == list:
                if type(data[0]) == Asm:
                    self.asm += data[0].asm
                else:
                    self.asm.append([str(i) for i in data])

    def __str__(self):
        return self.get_asm(ind=4)

    def get_asm(self, ind=4):
        asm = ""
        for i, line in enumerate(self.asm):
            asm += self.concat_instrs(line, ind=ind, end=("" if i == (len(self.asm) - 1) else "\n"))
        return asm

    def get_asm_full(self, template=TEMPLATE, s:str="_entry", t:str="_type", nasm_args:list[str]=["default rel"]) -> str:
        asm = Asm([self, [RET]]).get_asm(ind=4)
        return template.format(s=s, t=t, tn=self.eval_type, ts=self.eval_type_str, nasm_args="\n".join(nasm_args), asm=asm)

    def write(self, path):
        with open(path, "w") as file:
            file.write(self.get_asm_full())
    

def offset(reg, nbytes):
    return "[" + reg + "+" + str(nbytes*8) + "]"