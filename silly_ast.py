from lark import ast_utils, Transformer
from silly_types import *
from silly_env import Env

# abstract ast class
class _Ast(ast_utils.Ast):
    pass

# abstract expr class
class _Expr(_Ast):
    def check_typing(self, env) -> bool:
        raise Exception("cannot check typing of abstract expr")
    def check_binding(self, env) -> bool:
        raise Exception("cannot check binding of abstract expr")
    def has_side_effects(self, env) -> bool:
        return True
    def check_errs(self, env) -> bool:
        for f in [self.check_typing, self.check_binding]:
            assert f()
    def get_eval_type(self, env:dict[str, "_Expr"]) -> int:
        raise Exception("cannot get eval type of abstract expr")


# abstract literal class
class _Lit(_Expr):
    def __init__(self, v):
        self.v = v
    def check_typing(self, env:Env) -> bool:
        return True
    def check_binding(self, env:Env) -> bool:
        return True
    def has_side_effects(self, env) -> bool:
        return False
    def get_eval_type(self, env:Env) -> int:
        return self.__class__.evals

class Num(_Lit):
    evals = NUM

class Bool(_Lit):
    evals = BOOL

class Str(_Lit):
    evals = STR

class _Op(_Expr):
    pass

# abstract operator class
class _OpN(_Op):
    def __init__(self, *args:tuple[_Expr]):
        self.es:tuple[_Expr] = args
    def get_eval_type(self, env:Env) -> int:
        return self.__class__.evals
    def check_typing(self, env:Env) -> bool:
        for i in range(len(self.es)):
            if not (self.es[i].check_typing(env) and 
                    self.es[i].get_eval_type(env) == self.__class__.takes[i]):
                return False
        return True
    def check_binding(self, env:Env) -> bool:
        for i in range(len(self.es)):
            if not (self.es[i].check_binding(env) and 
                    self.es[i].get_eval_type(env) == self.__class__.takes[i]):
                return False
        return True
    def has_side_effects(self, env) -> bool:
        for e in self.es:
            if e.has_side_effects():
                return True
        return False

# abstract mono operator class
class _Op1(_OpN):
    pass

class Not(_Op1):
    takes = [BOOL]
    evals =  BOOL

class Neg(_Op1):
    takes = [NUM]
    evals =  NUM

class _Op2(_OpN):
    pass

class And(_Op2):
    takes = [BOOL, BOOL]
    evals = BOOL

class Or(_Op2):
    takes = [BOOL, BOOL]
    evals = BOOL

class Xor(_Op2):
    takes = [BOOL, BOOL]
    evals = BOOL

class Add(_Op2):
    takes = [NUM, NUM]
    evals = NUM

class Sub(_Op2):
    takes = [NUM, NUM]
    evals = NUM

class Mul(_Op2):
    takes = [NUM, NUM]
    evals = NUM

class Div(_Op2):
    takes = [NUM, NUM]
    evals = NUM

class Pow(_Op2):
    takes = [NUM, NUM]
    evals = NUM

class Gr(_Op2):
    takes = [NUM, NUM]
    evals = BOOL

class Geq(_Op2):
    takes = [NUM, NUM]
    evals = BOOL

class Lt(_Op2):
    takes = [NUM, NUM]
    evals = BOOL

class Leq(_Op2):
    takes = [NUM, NUM]
    evals = BOOL

class Eq(_Op2): # boolean equality operator 
    evals = BOOL

class Neq(_Op2):
    evals = BOOL

class If(_Expr):
    def __init__(self, c:_Expr, t:_Expr, f:_Expr):
        self.c = c
        self.t = t
        self.f = f
    def get_eval_type(self, env: dict[str, "_Expr"]) -> int:
        return self.t.get_eval_type(env)
    def check_typing(self, env) -> bool:
        return (self.c.check_typing(env) and
                self.t.check_typing(env) and
                self.f.check_typing(env) and
                self.c.get_eval_type(env) == BOOL and
                self.t.get_eval_type(env) == self.f.get_eval_type(env))

class _Let(_Expr):
    def __init__(self, *args) -> None:
        #print(args)
        self.id:str = args[0] 
        self.ids:list[_Expr] = list(args[1:-2]) # any ids for closure
        self.e0:_Expr = args[-2] # expr that is bound to id
        self.e1:_Expr = args[-1] # expr that is evaluated with x bound to e0 
    def get_eval_type(self, env:Env) -> int:
        return self.e1.get_eval_type(env.ext(Env({self.id:self.e0})))

class _Call(_Expr):
    def __init__(self, *args):
        self.id:str = args[0]
        self.es:list[_Expr] = list(args[1:])
    def get_eval_type(self, env:Env) -> int:
        return env.lookup(self.id).get_eval_type(env)

class Var(_Call):
    pass

class LetVar(_Let):
    pass

class Fun(_Call):
    pass

class LetFun(_Let):
    pass

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
            pass
        return es[-1]