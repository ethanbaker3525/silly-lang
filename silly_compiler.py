from sys import argv
import silly_parser as parser
from silly_ast import _Expr, _Lit, _Op2, _Op2Num, _Op1, _OpN
from silly_ast import *
from silly_asm import *
from silly_types import get_type_str

class Env:
    def __init__(self, binds={}):
        self.binds = binds
    def __str__(self):
        return str(self.binds)
    def lookup(self, _id):
        return self.binds[_id]
    def ext(self, ids:list[str] | str, es:list[_Expr] | _Expr):
        if type(ids) != list:
            ids = [ids]
        if type(es) != list:
            es = [es]
        l = len(ids)
        assert l == len(es)
        binds = dict(self.binds)
        for i in range(l):
            binds[ids[i]] = es[i]
        return Env(binds=self.binds)

def compile(e:_Expr) -> Asm:
    et = e.get_eval_type({})
    return Asm(
        [compile_env(e, Env())], 
        eval_type=et, 
        eval_type_str=get_type_str(et))

def compile_env(e, env) -> Asm:
    match e:
        case _Lit():
            return Asm([
                [MOV, RAX, val_to_bits(e.v)]])
        case _Op1():
            return compile_op1(e, e.es[0], env)
        case _Op2():
            return compile_op2(e, e.es[0], e.es[1], env)
        case If():

            """       c_asm = self.es[0].comp(env)
        t_asm = self.es[1].comp(env)
        f_asm = self.es[2].comp(env)
        t_lbl = gensym("if") # label to jump to for true
        e_lbl = gensym("if") # end
        return asm(
            (c_asm),
            ("cmp", "rax", val_to_bits(True)),
            ("je", t_lbl),
            (f_asm),
            ("jmp", e_lbl),
            (label(t_lbl)),
            (t_asm),
            (label(e_lbl)),
            c = "if"
        )"""
            lbt = gensym("if")
            lbe = gensym("if")
            return Asm([
                [compile_env(e.es[0], env)],
                [CMP, RAX, val_to_bits(True)],
                [JE,  lbt],
                [compile_env(e.es[2], env)],
                [JMP, lbe],
                [LBL, lbt],
                [compile_env(e.es[1], env)],
                [LBL, lbe]])
        case _:
            raise Exception("cannot compile " + str(e))

def compile_op1(op, e0, env):
    match op:
        case Neg(e):
            return Asm([
                [compile_env(e0, env)],
                [NOT, RAX],
                [INC, RAX]])
        case Not(e):
            return Asm([
                [compile_env(e, env)],
                [XOR, RAX, 0x1]])

def compile_op2(op, e0, e1, env):
    match op:
        case _Op2Num():
            return compile_op2num(op, e0, e1, env)
        case Eq():
            return Asm([
                [compile_env(e0)],
                [PUSH,  RAX],
                [compile_env(e1)],
                [POP,   R8],
                [CMP,   RAX, R8],
                [MOV,   RAX, val_to_bits(False)],
                [MOV,   R8, val_to_bits(True)],
                [CMOVE, RAX, R8]])

def compile_op2num(op, e0, e1, env):
    asm_es = Asm([
        [compile_env(e1, env)],
        [PUSH, RAX],
        [compile_env(e0, env)]])
    match op:
        case Add():
            asm_op = Asm([
                [POP, R8],
                [ADD, RAX, R8]])
        case Sub():
            asm_op = Asm([
                [POP, R8],
                [SUB, RAX, R8]])
        case Mul():
            asm_op = Asm([
                [POP, R8],
                [MUL, R8]])
        case Div():
            asm_op = Asm([
                [CQO],
                [POP, R8],
                [DIV, R8]])
        case Pow():
            raise Exception("pow unimplemented")
    return Asm([
        [asm_es],
        [asm_op]])

# utility functions

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

if __name__ == "__main__":
    EXT = "silly"
    if len(argv) == 2: # if not one cmdline arg do nothing
        if argv[1][-len(EXT):] == EXT: # if is .silly file
            fname_asm = None # then we dont want to make an asm
            fname_silly = argv[1]
        else:
            fname_asm = argv[1]
            fname_silly = argv[1].split("/")[2][:-len("asm")] + EXT
        with open(fname_silly, "r") as f:
            p = parser.Parser()
            p.parse(f.read())
            #print(p.p.pretty())
            ast = p.to_ast()
            asm = compile(ast)
        if fname_asm == None:
            print(asm.get_asm_full()) # printing asm instead of making .asm file
        else:
            with open(fname_asm, "w") as file:
                file.write(asm)


    


