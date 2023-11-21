from sys import argv

from silly_parser import *
from silly_ast import (
    _Expr as Expr,
    _Lit as Lit,
    _Op2 as Op2,
    _Op1 as Op1, 
    _OpN as OpN,
    _Let as Let)
from silly_ast import *
from silly_asm import *
from silly_env import *
from silly_types import get_type_str

def comp(e:Expr) -> Asm:
    et = e.get_eval_type({})
    return Asm(
        [comp_env(e, CEnv([]))], 
        eval_type=et, 
        eval_type_str=get_type_str(et))

def comp_env(e, env:CEnv) -> Asm:
    match e:
        case Lit():
            return Asm([
                [MOV, RAX, val_to_bits(e.v)]])
        case Var():
            return Asm([
                [MOV, RAX, offset(RSP, env.lookup(e.id))]
            ])
        case Op1():
            return comp_op1(e, e.es[0], env)
        case Op2():
            return comp_op2(e, e.es[0], e.es[1], env)
        case If():
            lbt = gensym("if")
            lbe = gensym("if")
            return Asm([
                [comp_env(e.es[0], env)],
                [CMP, RAX, val_to_bits(True)],
                [JE,  lbt],
                [comp_env(e.es[2], env)],
                [JMP, lbe],
                [LBL, lbt],
                [comp_env(e.es[1], env)],
                [LBL, lbe]])
        case Let():
            return comp_let(e, e.id, e.ids, e.e0, e.e1, env)
        case Fun():
            raise Exception("unimplemented")
        case _:
            raise Exception("cannot comp " + str(e))

def comp_let(x:Expr, xid:str, fvars:list[Var], e0:Expr, e1:Expr, env:CEnv):
    match x:
        case LetVar():
            return Asm([
                [comp_env(e0, env)],
                [PUSH, RAX],
                [comp_env(e1, env.ext(CEnv([xid])))],
                [ADD, RSP, 8]])
        case LetFun():
            raise Exception("unimplemented")

def comp_op1(op, e0, env:CEnv):
    match op:
        case Neg():
            return Asm([
                [comp_env(e0, env)],
                [NOT, RAX],
                [INC, RAX]])
        case Not():
            return Asm([
                [comp_env(e0, env)],
                [XOR, RAX, 0x1]])

def comp_op2(op, e0, e1, env:CEnv):
    asm_es = Asm([
        [comp_env(e1, env)],
        [PUSH, RAX],
        [comp_env(e0, env.add_offset(1))]])
    match op:
        case Add(): # e0 + e1
            return Asm([
                [asm_es],
                [POP, R8],
                [ADD, RAX, R8]])
        case Sub(): # e0 - e1
            return Asm([
                [asm_es],
                [POP, R8],
                [SUB, RAX, R8]])
        case Mul(): # e0 * e1
            return Asm([
                [asm_es],
                [POP, R8],
                [MUL, R8]])
        case Div(): # e0 / e1
            return Asm([
                [asm_es],
                [CQO],
                [POP, R8],
                [DIV, R8]])
        case Pow(): # e0 ^ e1
            raise Exception("unimplemented")
        case Gr():
            raise Exception("unimplemented") # maybe sepparate the funs that return int vs bool for simpler code
        case Geq():
            raise Exception("unimplemented") 
        case Lt():
            raise Exception("unimplemented") 
        case Leq():
            raise Exception("unimplemented") 
        case Eq(): # e0 = e1
            return Asm([
                [asm_es],
                [POP,   R8],
                [CMP,   RAX, R8],
                [MOV,   RAX, val_to_bits(False)],
                [MOV,   R8, val_to_bits(True)],
                [CMOVE, RAX, R8]])

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
            p = Parser()
            p.parse(f.read())
            #print(p.p.pretty())
            ast = p.to_ast()
            asm = comp(ast)
        if fname_asm == None:
            print(asm.get_asm_full()) # printing asm instead of making .asm file
        else:
            with open(fname_asm, "w") as file:
                file.write(asm.get_asm_full())


    


