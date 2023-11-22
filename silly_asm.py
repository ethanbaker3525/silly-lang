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
LEA   = "lea"

# label instructions
LBL = "."
FUN = "_"
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

# TODO make cleaner by adding sector class

class Asm:

    def __init__(self, asm:list[list], eval_type:int=-1, eval_type_str="", sect="entry"):
        self.eval_type=eval_type
        self.eval_type_str=get_type_str(eval_type)
        self.sects = {sect:[]}
        print(asm)
        for line in asm:
            assert type(asm) == list
            # adding asm
            if type(line[0]) == Asm:
                assert len(line) == 1
                #print(self.sects)
                for sect_str in line[0].sects.keys():
                    print(sect_str)
                    if not sect_str in self.sects:
                        self.sects[sect_str] = []
                    self.sects[sect_str] += line[0].sects[sect_str]
            # adding instructions
            elif type(line[0]) == str:
                self.sects[sect].append([str(i) for i in line])

        #print(self.sects)

    def __str__(self):
        #return self.get_asm_str(-1, "none", ind=4)
        return str(self.sects)

    def set_sect(self, sect):
        newlines = []
        for s in self.sects.values():
            for lines in s:
                newlines += lines
        #print(newlines)
        self.sects = {sect:[newlines]}
        #print(self.sects)

    def get_line_str(self, line, ind=4):
        #print(line)
        s = " " * ind
        #print(instrs)
        if line[0] == LBL:
            s = LBL + line[1] + ":"
        elif line[0] in [RET]:
            s += line[0]
        elif line[0] in [JMP, JE, JNE, JG, JGE, JL, JLE, JZ, JNZ]:
            s += line[0] + " ." + line[1]
        else:
            s += line[0] + " " + ", ".join(line[1:])
        return s

    def get_sect_str(self, sect, ind=4):
        #print(self.sects[sect])
        lines = [self.get_line_str(line, ind=ind) for line in self.sects[sect]]
        #print(lines)
        return "_"+ sect + ":" + "\n" + "\n".join(lines)

    def get_asm_str(self, eval_type, eval_type_str, ind=4, entry_lbl="entry", type_lbl="type", asmc_args=["default rel"]):
        TEMPLATE = (
        "global _{entry_lbl}\n"
        "global _{type_lbl}\n"
        "{asmc_args}\n"
        "\nsection .data\n"
        "_{type_lbl}: db {eval_type} ; eval type is {eval_type_str}\n"
        "\nsection .text\n"
        "{asm}")
        
        sects = self.sects.keys()
        print(sects)
        #assert entry_lbl in sects
        asm = "\n".join([self.get_sect_str(sect, ind=ind) for sect in sects])
           

            
        return TEMPLATE.format(asm=asm, entry_lbl=entry_lbl, type_lbl=type_lbl, eval_type=self.eval_type, eval_type_str=self.eval_type_str, asmc_args="\n".join(asmc_args))

    def write(self, path):
        with open(path, "w") as file:
            file.write(self.get_asm_str(1, "num"))
    

def offset(reg, nbytes):
    return "[" + reg + "+" + str(nbytes*8) + "]"


if __name__ == "__main__":
    s0 = Asm([
        [MOV, RAX, 11],
        [MOV, RAX, 12]
    ])
    print(s0)
    s1 = Asm([
        [s0],
        [MOV, RAX, 13],
        [RET]
    ])
    print(s1)
    s2 = Asm([
        [MOV, RAX, 13]
    ], sect="test")
    print(s2)
    s3 = Asm([
        [s2],
        [s1]
    ])
    print(s3)
    