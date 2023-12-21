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
from silly_env import *
from silly_types import get_type_str
from silly_utils import *
from silly_err import CompErr
from silly_ast_utils import check_typing, get_eval_type

def comp(e:Expr, do_type_check=False) -> asm:
    # checks
    if do_type_check and not check_typing(e, {}):
        raise CompErr("bad typing")
    et = 2 #get_eval_type(e, {}) ALWAYS EVALS TO INT
    # compiling
    s = asm([
        [comp_env(e, CEnv([]))]
        ])
    s["EVAL_TYPE"] = et
    return s

def comp_env(e, env:CEnv) -> dict:
    match e:
        case Lit():
            return asm([
                [MOV, RAX, val_to_bits(e.v)]])
        case Var():
            return asm([
                [MOV, RAX, offset(RSP, env.lookup(e.id))]])
        case Fun():
            return comp_fun(e, e.id, e.es, env)
        case Op1():
            return comp_op1(e, e.es[0], env)
        case Op2():
            return comp_op2(e, e.es[0], e.es[1], env)
        case If():
            lbt = genlbl("if")
            lbe = genlbl("ifend")
            return asm([
                [comp_env(e.c, env)],
                [CMP, RAX, val_to_bits(True)],
                [JE,  lbt],
                [comp_env(e.f, env)],
                [JMP, lbe],
                [lbt],
                [comp_env(e.t, env)],
                [lbe]])
        case Let():
            return comp_let(e, e.id, e.ids, e.e0, e.e1, env)
        case _:
            raise Exception("cannot comp " + str(e))

def comp_fun(f, xid, es, env):
    match xid:
        case "rb":
            assert len(es) == 0
            return asm([
                [pad_stack()],
                [CALL, "read_byte"],
                [unpad_stack()]
            ])
        case "wb":
            assert len(es) == 1
            return asm([
                [pad_stack()],
                [comp_env(es[0], env)],
                [MOV, RDI, RAX],
                [CALL, "write_byte"],
                [unpad_stack()]
            ])
        case "pb":
            assert len(es) == 0
            return asm([
                [pad_stack()],
                [CALL, "peek_byte"],
                [unpad_stack()]
            ])
        case fid:
            env.lookup(fid) # make sure fid in is scope
            return asm([
               *[asm([
                [comp_env(e, env)], # evaluating and pushing params
                [PUSH, RAX]]) 
                for e in es],
                [CALL, label(fid)], # calling the function
                [ADD, RSP, (8*len(es))]])

def comp_let(x:Expr, xid:str, fvars:list[Var], e0:Expr, e1:Expr, env:CEnv):
    match x:
        case LetVar():
            return asm([
                [comp_env(e0, env)],
                [PUSH, RAX],
                [comp_env(e1, env.ext(CEnv([xid])))],
                [ADD, RSP, 8]])
        case LetFun():
            funlbl = label(xid)
            fun = asm([
                [comp_env(e0, env.ext(CEnv([xid] + [fvar.id for fvar in fvars])).add_offset(1))] # last param first
            ], label=funlbl, force_label=True)
            return asm([
                [LEA, RAX, funlbl],
                [PUSH, RAX],
                [comp_env(e1, env.ext(CEnv([xid])))],
                [ADD, RSP, 8],
                [fun]
            ])

def comp_op1(op, e0, env:CEnv):
    match op:
        case Neg():
            return asm([
                [comp_env(e0, env)],
                [NOT, RAX],
                [INC, RAX]])
        case Not():
            return asm([
                [comp_env(e0, env)],
                [XOR, RAX, 0x1]])
        case _ :
            raise CompErr("cannot comp " + str(op))

def comp_op2(op, e0, e1, env:CEnv):
    asm_es = asm([
        [comp_env(e1, env)],
        [PUSH, RAX],
        [comp_env(e0, env.add_offset(1))]])
    match op:
        case Add(): # e0 + e1
            return asm([
                [asm_es],
                [POP, R8],
                [ADD, RAX, R8]])
        case Sub(): # e0 - e1
            return asm([
                [asm_es],
                [POP, R8],
                [SUB, RAX, R8]])
        case Mul(): # e0 * e1
            return asm([
                [asm_es],
                [POP, R8],
                [MUL, R8]])
        case Div(): # e0 / e1
            return asm([
                [asm_es],
                [CQO],
                [POP, R8],
                [DIV, R8]])
        case Pow(): # e0 ^ e1
            raise NotImplementedError("^")
        case Gr():
            raise NotImplementedError(">")
        case Geq():
            raise NotImplementedError(">=")
        case Lt():
            raise NotImplementedError("<")
        case Leq():
            raise NotImplementedError("<=")
        case And():
            return asm([
                [asm_es],
                [POP, R8],
                [AND, RAX, R8]])
        case Or():
            return asm([
                [asm_es],
                [POP, R8],
                [OR, RAX, R8]])
        case Xor():
            return asm([
                [asm_es],
                [POP, R8],
                [XOR, RAX, R8]])
        case Eq(): # e0 = e1
            return asm([
                [asm_es],
                [POP,   R8],
                [CMP,   RAX, R8],
                [MOV,   RAX, val_to_bits(False)],
                [MOV,   R8, val_to_bits(True)],
                [CMOVE, RAX, R8]])
        case Neq():
            return asm([
                [asm_es],
                [POP,   R8],
                [CMP,   RAX, R8],
                [MOV,   RAX, val_to_bits(True)],
                [MOV,   R8, val_to_bits(False)],
                [CMOVE, RAX, R8]])
        case _ :
            raise CompErr("cannot comp " + str(op))

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


    


