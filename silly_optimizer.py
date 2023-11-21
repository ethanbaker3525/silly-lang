from silly_ast import (
    _Ast as Ast,
    _Expr as Expr,
    _Lit as Lit,
    _Op2 as Op2,
    _Op1 as Op1, 
    _OpN as OpN,
    _Let as Let)
from silly_ast import *

def optimize_ast(ast:Ast) -> Ast:
    return ast