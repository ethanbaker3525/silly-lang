from lark import Lark, ast_utils, Transformer
from silly_utils import err, asm, gensym, label, val_to_bits, types
# type checking is done at compile time not execution time

# abstract ast class
class _Ast(ast_utils.Ast):
    pass

# abstract expr class
class _Expr(_Ast):
    def check_typing(self) -> bool:
        err("cannot check typing of abstract expr")
    def get_eval_type(self) -> int:
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
    def get_eval_type(self) -> int:
        return types[self.__class__.t]
    def eval(self, env):
        return self
    def comp(self, env):
        return asm(
            ("mov", "rax", val_to_bits(self.v)),
            c = self.__class__.t + " literal")

class Num(_Lit):
    t = "num" # evals to types["num"]

class Bool(_Lit):
    t = "bool" # evals to types["bool"]

class Str(_Lit):
    t = "str" # evals to types["str"]

# abstract operator class
class _OpN(_Expr):
    def __init__(self, *args:tuple[_Expr]):
        self.es:tuple[_Expr] = args

# abstract mono operator class
class _Op1(_OpN):
    t = None # type that the op takes and returns
    def check_typing(self) -> bool: # op1s have correct typing if e[0] has correct typing and e[0]'s type = t
        return (
            self.es[0].check_typing() and
            self.es[0].get_eval_type() == types[self.__class__.t]
        )
    def get_eval_type(self) -> int:
        return types[self.__class__.t]

class Not(_Op1):
    t = "bool"
    def eval(self, env) -> _Expr:
        return Bool(not self.es[0].v)
    def comp(self, env) -> str:
        return asm(
            (self.es[0].comp(env)),
            ("xor", "rax", "0x1"),
            c = "boolean not"
        )

class Neg(_Op1):
    t = "num"
    def eval(self, env) -> _Expr:
        return Num(- self.es[0].v)
    def comp(self, env) -> str:
        return asm(
            (self.es[0].comp(env)),
            ("not", "rax"),
            ("inc", "rax"), c = "int negation"
        )
    
# abstract binary operator class
class _Op2(_OpN):
    pass

# abstract numeric binary operator class (+, -, *...)
class _Op2Num(_Op2):
    def check_typing(self) -> bool:
        return (
            self.es[0].check_typing() and
            self.es[1].check_typing() and
            self.es[0].get_eval_type() == types["num"] and
            self.es[1].get_eval_type() == types["num"]
        )
    def get_eval_type(self) -> int:
        return types["num"]
    def eval(self, env):
        y = self.es[1].eval(env).v
        x = self.es[0].eval(env).v
        return Num(self.__class__.e_op(x, y))
    def comp(self, env) -> str:
        return asm( # TODO should be able to do this without push/ pop
            (self.es[1].comp(env)),
            ("push", "rax"),
            (self.es[0].comp(env)),
            ("pop", "r8"),
            (self.__class__.c_op, "rax", "r8"),
            c = "int " + self.__class__.c_op
        )

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
            ("mul", "r8"),
            c = "int mul"
        )

class Div(_Op2Num):
    e_op = lambda x, y: x / y
    def comp(self, env) -> str:
        return asm(
            (self.es[1].comp(env)),
            ("push", "rax"),
            (self.es[0].comp(env)),
            ("cqo"),
            ("pop", "r8"),
            ("div", "r8"),
            c = "int div"
        )

class Pow(_Op2Num): # TODO
    e_op = lambda x, y: x + y
    c_op = "add"

class Eq(_Op2): # boolean equality operator
    def check_typing(self) -> bool: # true if x has good typing and y has good typing and x_type = y_type
        return (
            self.es[0].check_typing() and
            self.es[1].check_typing() and
            self.es[0].get_eval_type() == self.es[1].get_eval_type()
        )
    def get_eval_type(self) -> int:
        return types["bool"]
    def eval(self, env):
        y = self.es[1].eval(env).v
        x = self.es[0].eval(env).v
        return Bool(x == y)
    def comp(self, env) -> str:
        asm0 = (self.es[0].comp(env))
        asm1 = (self.es[1].comp(env))
        return asm(
            (asm0),
            ("push", "rax"),
            (asm1),
            ("pop", "r8"),
            ("cmp", "rax", "r8"),
            ("mov", "rax", val_to_bits(False)),
            ("mov", "r8", val_to_bits(True)),
            ("cmove", "rax", "r8"),
            c = "bool equals"
        )

class If(_OpN):
    def check_typing(self) -> bool:
        return (
            self.es[0].check_typing() and
            self.es[0].get_eval_type() == types["bool"] and
            self.es[1].check_typing() and 
            self.es[2].check_typing() and 
            self.es[1].get_eval_type() == self.es[2].get_eval_type()
        )
    def get_eval_type(self) -> int:
        #assert self.es[1].get_eval_type() == self.es[2].get_eval_type()
        return self.es[1].get_eval_type()

    def eval(self, env) -> "_Expr":
        if self.es[0].eval().v:
            return self.es[1]
        return self.es[2]
    
    def comp(self, env) -> str:
        c_asm = self.es[0].comp(env)
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

        )

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