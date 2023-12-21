from silly_parser import Parser
from silly_ast import (
    _Expr as Expr,
    _Lit as Lit,
    _Unit as Unit,
    _Multi as Multi,
    _Op2 as Op2,
    _Op1 as Op1, 
    _OpN as OpN,
    _Let as Let,
    _Call as Call)
from silly_ast import *
from silly_env import *
from silly_utils import *
from silly_types import *

def ext(tenv0:dict[str, int], tenv1:dict[str, int]): # extends tenv0 with tenv1
    return tenv0 | tenv1

""" GETS THE EVALUATION TYPE OF A GIVEN EXPR (e) IN AN ENVIROMENT (tenv)"""
def get_eval_type(e:Expr, tenv:dict[str, int]):
    match e:
        case Lit():
            return get_eval_type_lit(e)
        case Multi():
            return get_eval_type_multi(e)

        case Op1():
            return get_eval_type_op1(e)
        case Op2():
            return get_eval_type_op2(e)
        case If():
            try:
                t = get_eval_type(e.t, tenv)
            except KeyError:
                t = get_eval_type(e.f, tenv)
            finally:
                return t
        case Let():
            return get_eval_type(e.e1, ext(tenv, {e.id: get_eval_type(e.e0, tenv)})) # TODO this will only work for functions if you use closures
        case Call():
            return tenv[e.id]
        case _:
            raise Exception(f"cannot get eval type of {e}")
def get_eval_type_multi(e:Multi, tenv:dict[str, int]):
    match e:
        case Cons():
            raise NotImplementedError()
            #return get_eval_type(e.es[0] tenv)
        case _:
            raise Exception(f"cannot get eval type of multi {e}")

def get_eval_type_lit(e:Lit):
    match e:
        case Num():
            return NUM
        case Bool():
            return BOOL
        case Unit():
            return UNIT
        case _:
            raise Exception(f"cannot get eval type of lit {e}")

def get_eval_type_op1(e:Op1):
    match e:
        case Not():
            return BOOL
        case Neg():
            return NUM
        case _:
            raise Exception(f"cannot get eval type of op1 {e}")

def get_eval_type_op2(e:Op2):
    match e:
        case And() | Or() | Xor() | Gr() | Geq() | Lt() | Leq() | Eq() | Neq():
            return BOOL
        case Add() | Sub() | Mul() | Div() | Pow():
            return NUM
        case _:
            raise Exception(f"cannot get eval type of op2 {e}")

""" CHECKS THAT A GIVEN EXPR (e) IN AN ENVIROMENT (tenv) HAS CORRECT TYPING (ex. 1 + true | if 1 then 2 else true) """
def check_typing(e:Expr, tenv:dict[str, int]):
    match e:
        case Lit():
            return True
        case Op1():
            return check_typing_op1(e, tenv)
        case Op2():
            return check_typing_op2(e, tenv)
        case If(): # TODO this will cause problems with recursion
            return (check_typings([e.c, e.t, e.f], tenv) and
                    get_eval_type(e.c, tenv) == BOOL and
                    get_eval_type(e.t, tenv) == get_eval_type(e.f, tenv))
        case Let():
            return (check_typing(e.e0, tenv) and
                    check_typing(e.e1, ext(tenv, {e.id: get_eval_type(e.e0, tenv)})))
        case Call():
            return (check_typings(e.es, tenv))
        case _:
            raise Exception(f"cannot check eval type of {e}")

def check_typings(es:list[Expr], tenv:dict[str, int]): # check the typings of list of exprs, false if any have bad typing
    for e in es:
        if not check_typing(e, tenv):
            return False
    return True

def check_typing_op1(e:Expr, tenv:dict[str, int]):
    if not check_typings(e.es):
        return False
    match e: # then check that the op1 has the right typing
        case Not():
            return get_eval_type(e.es[0], tenv) == BOOL
        case Neg():
            return get_eval_type(e.es[0], tenv) == NUM

def check_typing_op2(e:Op2, tenv:dict[str, int]):
    if not check_typings(e.es, tenv):
        return False
    match e: # then check that the op2 has the right typing
        case And() | Or() | Xor(): # must take two bools
            return (get_eval_type(e.es[0], tenv) == BOOL and
                    get_eval_type(e.es[1], tenv) == BOOL)
        case Add() | Sub() | Mul() | Div() | Pow() | Gr() | Geq() | Lt() | Leq(): # must take two nums
            return (get_eval_type(e.es[0], tenv) == NUM and
                    get_eval_type(e.es[1], tenv) == NUM)
        case Eq() | Neq(): # must take two of the same type
            return get_eval_type(e.es[0], tenv) == get_eval_type(e.es[1], tenv)
        case _:
            raise Exception(f"cannot check eval type of op2 {e}")