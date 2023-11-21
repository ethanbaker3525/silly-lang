from sys import argv

from silly_parser import Parser
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

def interp(e:Expr) -> Expr:
    return interp_env(e, Env({}))

def interp_env(e:Expr, env:Env):
    match e:
        case Lit():
            return e
        case Var():
            return env.lookup(e.id) # no need to interp cause even if x holds a func, calling "x" will not eval
        case Op1():
            return interp_op1(e, e.es[0], env)
        case Op2():
            return interp_op2(e, e.es[0], e.es[1], env)
        case If():
            if interp_env(e.es[0], env).v:
                return interp_env(e.es[1], env)
            return     interp_env(e.es[2], env)
        case Let():
            return interp_let(e, e.id, e.ids, e.e0, e.e1, env)
        case Fun():
            return interp_fun(e, e.id, e.es, env)
        case _:
            raise Exception("cannot interpret '" + str(e) + "'")

def interp_let(x:Expr, xid:str, fvars:list[Var], e0:Expr, e1:Expr, env:Env):
    match x:
        case LetVar():
            return interp_env(e1, env.ext(Env({xid: interp_env(e0, env)})))
        case LetFun():
            ids = [var.id for var in fvars]
            return interp_env(e1, env.ext(Env({xid: Closure(ids, e0, env)})))

def interp_fun(e:Expr, fid:str, es:list[Expr], env:Env):
    match fid:
        case "print":
            pass
        case "input":
            pass
        case _:
            es = [interp_env(e, env) for e in es]
            cl = env.lookup(fid) # getting the closure from the env
            clenv = cl.bind(es)
            return interp_env(cl.e, env.ext(clenv)) # interp closure with bound params
            
def interp_op1(op:Expr, e:Expr, env:Env):
    match op:
        case Neg():
            return Num(- interp_env(e, env).v)
        case Not():
            return Bool(not interp_env(e, env).v)

def interp_op2(op:Expr, e0:Expr, e1:Expr, env:Env):
    v0 = interp_env(e0, env).v
    v1 = interp_env(e1, env).v
    match op:
        # arithmatic
        case Add():
            return Num(v0 + v1)
        case Sub():
            return Num(v0 - v1)
        case Mul():
            return Num(v0 * v1)
        case Div():
            return Num(v0 / v1)
        case Pow():
            return Num(v0 ** v1)
        # comparison
        case Gr():
            return Bool(v0 > v1)
        case Geq():
            return Bool(v0 >= v1)
        case Lt():
            return Bool(v0 < v1)
        case Leq():
            return Bool(v0 <= v1)
        # boolean
        case And():
            return Bool(v0 and v1)
        case Or():
            return Bool(v0 or v1)
        case Xor():
            return Bool((v0 and not v1) or (v1 and not v0))
        # equality
        case Eq():
            v0 = interp_env(e0, env).v
            v1 = interp_env(e1, env).v
            return Bool(v0 == v1)
        case Neq():
            v0 = interp_env(e0, env).v
            v1 = interp_env(e1, env).v
            return Bool(v0 != v1)

# utility functions
def str_res(x):
    match x:
        case Lit():
            return str(x.v)
        case Closure():
            return "closure"
        case _:
            raise Exception(x)

def interp_code(s, print_result=True, print_tree=False):
    p = Parser()
    p.parse(s)
    if print_tree:
        print(p.p.pretty()) 
    ast = p.to_ast()
    x = interp(ast)
    s = str_res(x)
    if print_result:
        print(s)
    return s

if __name__ == '__main__':
    
    if len(argv) == 1:
        s = input('> ')
        while True:
            interp_code(s)
            s = input('> ')
    else:
        with open(argv[1], "r") as file:
            interp_code(file.read())