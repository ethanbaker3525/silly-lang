from lark import ast_utils, Transformer
from silly_utils import err, asm, gensym, label, ext_env
from silly_types import TYPES as types

# abstract ast class
class _Ast(ast_utils.Ast):
    pass

# abstract expr class
class _Expr(_Ast):
    def check_typing(self, env) -> bool:
        err("cannot check typing of abstract expr")
    def check_binding(self, env) -> bool:
        err("cannot check binding of abstract expr")
    def check_errs(self, env) -> bool:
        return (
            self.check_typing() and
            self.check_binding())
    def get_eval_type(self, env:dict[str, "_Expr"]) -> int:
        err("cannot get eval type of abstract expr")


# abstract literal class
class _Lit(_Expr):
    __match_args__ = ("t", "v")
    def __init__(self, v):
        self.v = v
    def check_typing(self, env) -> bool:
        return True
    def check_binding(self, env) -> bool:
        return True
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return types[self.__class__.t]

class Num(_Lit):
    t = "num" # evals to types["num"]

class Bool(_Lit):
    t = "bool" # evals to types["bool"]

class Str(_Lit):
    t = "str" # evals to types["str"]

class _Op(_Expr):
    pass

# abstract operator class
class _OpN(_Op):
    def __init__(self, *args:tuple[_Expr]):
        self.es:tuple[_Expr] = args
    def check_typing(self, env) -> bool:
        return not False in [e.check_typing(env) for e in self.es]
    def check_binding(self, env) -> bool:
        return not False in [e.check_binding(env) for e in self.es]

# abstract mono operator class
class _Op1(_OpN):
    t = None # type that the op takes and returns
    def check_typing(self, env) -> bool: # op1s have correct typing if e[0] has correct typing and e[0]'s type = t
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == types[self.__class__.t]
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return types[self.__class__.t]

class Not(_Op1):
    t = "bool"

class Neg(_Op1):
    t = "num"
    
# abstract binary operator class
# TODO make this class work so you dont have code duplication in and, or, etc
class _Op2(_OpN):
    pass

class _Op2Bool(_Op2):
    pass

class And(_Op2Bool):
    pass

class Or(_Op2Bool):
    pass

class Xor(_Op2Bool):
    pass

# abstract numeric binary operator class (+, -, *...)
class _Op2Num(_Op2): # TODO make this class part of Op2 for clean code
    def check_typing(self, env) -> bool:
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == types["num"] and
            self.es[1].get_eval_type(env) == types["num"]
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return types["num"]

class Add(_Op2Num):
    pass

class Sub(_Op2Num):
    pass

class Mul(_Op2Num):
    pass

class Div(_Op2Num):
    pass

class Pow(_Op2Num):
    pass

class Gr(_Op2Num):
    pass

class Geq(_Op2Num):
    pass

class Lt(_Op2Num):
    pass

class Leq(_Op2Num):
    pass

class Eq(_Op2): # boolean equality operator 
    def check_typing(self, env) -> bool: # true if x has good typing and y has good typing and x_type = y_type
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == self.es[1].get_eval_type(env)
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return types["bool"]

class Neq(_Op2):
    pass

class If(_OpN):
    def check_typing(self, env) -> bool:
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == types["bool"] and
            self.es[1].get_eval_type(env) == self.es[2].get_eval_type(env)
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        #assert self.es[1].get_eval_type(env) == self.es[2].get_eval_type(env)
        return self.es[1].get_eval_type(env)

class _Let(_Expr):
    def __init__(self, *args) -> None:
        #print(args)
        self.id:str = args[0] 
        self.ids:list[_Expr] = list(args[1:-2]) # any ids for closure
        self.e0:_Expr = args[-2] # expr that is bound to id
        self.e1:_Expr = args[-1] # expr that is evaluated with x bound to e0 

class _Call(_Expr):
    def __init__(self, *args):
        self.id:str = args[0]
        self.es:list[_Expr] = list(args[1:])

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