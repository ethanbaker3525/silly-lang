from lark import Lark, ast_utils, Transformer
from silly_utils import err, asm
# type checking is done at compile time not execution time

class _Ast(ast_utils.Ast):
    pass

class _Expr(_Ast):
    def check_typing(self) -> bool:
        err("cannot check typing of abstract expr")
    def get_eval_type(self) -> str:
        err("cannot get eval type of abstract expr")
    def eval(self, env) -> "_Expr": 
        err("cannot evaluate abstract expr")
    def comp(self, env) -> str:
        err("cannot compile abstract expr")


# abstract literal class
class _Lit(_Expr):
    def __init__(self, v):
        self.v = v
    def check_typing(self) -> bool:
        return True
    def get_eval_type(self) -> str:
        return self.__class__.t
    def eval(self, env):
        return self
    def comp(self, env):
        return asm(
            ("mov", "rax", self.v))

class Num(_Lit):
    t = "num"

class Bool(_Lit):
    t = "bool"

class Str(_Lit):
    t = "str"

# abstract operator class
class _Op(_Expr):
    comp_op = lambda ls: err()
    eval_op = lambda ls: err()
    def __init__(self, *args:tuple[_Expr], **kwargs):
        super().__init__(**kwargs)
        self.es:tuple[_Expr] = args
            
    def eval(self):
        return self.__class__.op([e.eval() for e in self.es])

# abstract single operator class
class _Op1(_Op):
    pass

class Neg(_Op1):
    def check_typing(self) -> bool:
        return (
            self.es[0].check_typing()
        and self.es[0].get_eval_type() == "num")
    def get_eval_type(self) -> str:
        return "num"
    def comp(self):
        return 

class Not(_Op1):
    op    = lambda ls: Num(not ls[0].v)
    op_ts = [Bool]
    t     =  Bool
    
# abstract binary operator class
class _Op2(_Op):
    pass

class _Op2Num(_Op2):
    def check_typing(self) -> bool:
        return (
            self.es[0].check_typing()
        and self.es[1].check_typing()
        and self.es[0].get_eval_type() == "num"
        and self.es[1].get_eval_type() == "num")
    def get_eval_type(self) -> str:
        return "num"
    def eval(self, env):
        y = self.es[1].eval(env).v
        x = self.es[0].eval(env).v
        return Num(self.__class__.e_op(x, y))
    def comp(self, env) -> str:
        return asm(
            (self.es[1].comp(env)),
            ("push", "rax"),
            (self.es[0].comp(env)),
            ("pop", "r8"),
            (self.__class__.c_op, "rax", "r8"))

# Num Ops
class Add(_Op2Num):
    e_op = lambda x, y: x + y
    c_op = "add"

class Sub(_Op2Num):
    e_op = lambda x, y: x - y
    c_op = "sub"

class Mul(_Op2Num):
    e_op = lambda x, y: x * y
    def comp(self, env) -> str:
        return asm(
            (self.es[1].comp(env)),
            ("push", "rax"),
            (self.es[0].comp(env)),
            ("pop", "r8"),
            ("mul", "r8"))

class Div(_Op2Num):
    e_op = lambda x, y: x / y
    def comp(self, env) -> str:
        return asm(
            (self.es[1].comp(env)),
            ("push", "rax"),
            (self.es[0].comp(env)),
            ("cqo"),
            ("pop", "r8"),
            ("div", "r8"))

class Pow(_Op2Num):
    e_op = lambda x, y: x + y
    c_op = "add"

class Eq(_Op2):
    op = lambda ls: Bool(ls[0].v == ls[1].v)

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