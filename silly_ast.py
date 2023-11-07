import sys
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

def assert_es_match_ts(es, ts):
    for i in range(len(es)):
        if not issubclass(es[i].t, ts[min(i, len(ts)-1)]):
            print(str(es) + " doesnt match " + str(ts))
            exit()

def assert_ts_match(ts):
    for i in range(len(ts) - 1):
        if ts[i] != ts[i + 1]:
            print(str(ts[i]) + " doesnt match " + str(ts[i + 1]))
            exit()

def lookup(v, env) -> "_Expr":
    if v in env.keys():
        return env[v]
    return _Err(str(v) + " is not in scope for env " + str(env))

class _Ast(ast_utils.Ast):
    pass

class _Expr(_Ast):
    def __init__(self, env={}):
        self.env = env
    def eval(self): # returns the evaluated expr
        return _Err("cannot eval abstract expr")

class _Err(_Expr):
    def __init__(self, msg):
        super().__init__()
        self.v = msg
        self.t = self.__class__
    def eval(self): # returns the evaluated expr
        return self

# abstract literal class
class _Lit(_Expr):
    def __init__(self, v, **kwargs):
        super().__init__(**kwargs)
        self.v = v
        self.t = self.__class__
    def eval(self):
        return self

class Num(_Lit):
    pass

class Bool(_Lit):
    pass

class Str(_Lit):
    pass

# abstract operator class
class _Op(_Expr):
    op = lambda ls: _Err()
    op_ts = [_Expr]
    t = _Err
    def __init__(self, *args:tuple[_Expr], **kwargs):
        super().__init__(**kwargs)
        self.es:tuple[_Expr] = args
        # type checking
        assert_es_match_ts(self.es, self.__class__.op_ts)
            
    def eval(self):
        return self.__class__.op([e.eval() for e in self.es])

# abstract single operator class
class _Op1(_Op):
    pass

class Neg(_Op1):
    op     = lambda ls: Num(- ls[0].v)
    op_ts  = [Num]
    t      =  Num

class Not(_Op1):
    op    = lambda ls: Num(not ls[0].v)
    op_ts = [Bool]
    t     =  Bool
    
# abstract binary operator class
class _Op2(_Op):
    pass

class _Op2Num(_Op2):
    op_ts = [Num]
    t     =  Num

# Num Ops
class Add(_Op2Num):
    op = lambda ls: Num(ls[0].v +  ls[1].v)

class Sub(_Op2Num):
    op = lambda ls: Num(ls[0].v -  ls[1].v)

class Mul(_Op2Num):
    op = lambda ls: Num(ls[0].v *  ls[1].v)

class Div(_Op2Num):
    op = lambda ls: Num(ls[0].v /  ls[1].v)

class Pow(_Op2Num):
    op = lambda ls: Num(ls[0].v ** ls[1].v)

class Eq(_Op2):
    op = lambda ls: Bool(ls[0].v == ls[1].v)
    op_ts = [_Expr]
    t = _Expr
    def __init__(self, *args:tuple[_Expr], **kwargs):
        super().__init__(*args, **kwargs) # getting self.es
        if isinstance(self.es[0], Id): # if false, expr is boolean equality check
            x = lookup(self.es[0].v, self.env) # lookup id in env
            if isinstance(x, _Err): # id does not exist, we must assign it
                self.env[self.es[0].v] = self.es[1]
                self.is_eq_check = False
                self.t = self.es[1].t
                return
        assert_ts_match([self.es[0].t, self.es[1].t])
        self.is_eq_check = True
        self.t = Bool

    def eval(self):
        if self.is_eq_check:
            return super().eval()
        return lookup(self.es[0].v, self.env).eval()

class Id(_Expr):
    def __init__(self, v, **kwargs):
        super().__init__(**kwargs)
        self.v = v
        self.t = lookup(self.v, self.env).t
    def eval(self):
        return lookup(self.v, self.env).eval()

class If(_Op):
    op_ts = [Bool, _Expr]

    def __init__(self, *args: tuple[_Expr], **kwargs):
        super().__init__(*args, **kwargs)

    def op(ls):
        if ls[0].eval().v:
            return ls[1].eval()
        return ls[2].eval()

class ToAst(Transformer):

    def ID(self, s):
        return str(s)

    def STR(self, s):
        return s[1:-1]

    def NUM(self, n):
        return int(n)
    
    def BOOL(self, n):
        if n == "true":
            return True
        return False

    def prog(self, es):
        for i in range(len(es) - 1):
            es[i+1].env = es[i].env

        return es[-1]