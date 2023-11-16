from lark import Lark, ast_utils, Transformer
from silly_utils import err, asm, gensym, label, ext_env
from silly_types import TYPES as types
# val_to_bits
# type checking is done at compile time not execution time

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
    def eval(self, env:dict[str, "_Expr"]) -> "_Expr": 
        err("cannot evaluate abstract expr")
    def comp(self, env) -> str:
        err("cannot compile abstract expr")


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
    def eval(self, env:dict[str, _Expr]):
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
    def eval(self, env:dict[str, _Expr]) -> _Expr:
        return Bool(not self.es[0].v)
    def comp(self, env) -> str:
        return asm(
            (self.es[0].comp(env)),
            ("xor", "rax", "0x1"),
            c = "boolean not"
        )

class Neg(_Op1):
    t = "num"
    def eval(self, env:dict[str, _Expr]) -> _Expr:
        return Num(- self.es[0].v)
    def comp(self, env) -> str:
        return asm(
            (self.es[0].comp(env)),
            ("not", "rax"),
            ("inc", "rax"), c = "int negation"
        )
    
# abstract binary operator class
# TODO make this class work so you dont have code duplication in and, or, etc
class _Op2(_OpN):
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
    def eval(self, env:dict[str, _Expr]):
        x = self.es[0].eval(env)
        y = self.es[1].eval(env)
        return Num(self.__class__.e_op(x.v, y.v))
    def comp(self, env) -> str:
        return asm( # TODO should be able to do this without push/ pop (not really actually)
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
    def check_typing(self, env) -> bool: # true if x has good typing and y has good typing and x_type = y_type
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == self.es[1].get_eval_type(env)
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return types["bool"]
    def eval(self, env:dict[str, _Expr]):
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
    def check_typing(self, env) -> bool:
        return (
            super().check_typing(env) and
            self.es[0].get_eval_type(env) == types["bool"] and
            self.es[1].get_eval_type(env) == self.es[2].get_eval_type(env)
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        #assert self.es[1].get_eval_type(env) == self.es[2].get_eval_type(env)
        return self.es[1].get_eval_type(env)

    def eval(self, env:dict[str, _Expr]) -> "_Expr":
        if self.es[0].eval(env).v:
            return self.es[1].eval(env)
        x = self.es[2].eval(env)
        return x
    
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

class _Let(_Expr):
    pass

class Var(_Expr):
    def __init__(self, vid):
        self.id = vid
    def check_typing(self, env) -> bool:
        return True
    def check_binding(self, env) -> bool:
        return self.id in env.keys()
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return env[self.id].get_eval_type()
    def eval(self, env: dict[str, "_Expr"]) -> "_Expr":
        return env[self.id].eval(env)
    def comp(self, env) -> str:
        return super().comp(env) # TODO

class LetVar(_Expr):
    def __init__(self, vid:str, ve:_Expr, e:_Expr):
        self.id = vid
        self.ve = ve
        self.e = e
    def check_typing(self, env) -> bool:
        return (
            self.ve.check_typing(env) and
            self.e.check_typing(env)
        )
    def check_binding(self, env) -> bool:
        return (
            self.ve.check_binding(env) and
            self.e.check_binding(env)
        )
    def get_eval_type(self, env:dict[str, _Expr]) -> int:
        return self.es[1] # eval type of let id = e0 in e1 is type of e1
    def eval(self, env:dict[str, _Expr]) -> "_Expr":
        return self.e.eval(ext_env(env, self.id, self.ve.eval(env)))
    def comp(self, env) -> str:
        return super().comp(env) # TODO

# function call
class Fun(_Expr):
    def __init__(self, fid, *es): # f(expr0, expr1)
        self.id = fid # f
        self.es = es # expr0, expr1
    def check_typing(self, env) -> bool:
        return not False in [e.check_typing(env) for e in self.es]# TODO must check that bound vars are correct type too
    def check_binding(self, env) -> bool:
        return (
            (not False in [e.check_binding(env) for e in self.es]) and
            self.id in env.keys()
        )
    def get_eval_type(self, env: dict[str, "_Expr"]) -> int:
        return env[self.id].get_eval_type()
    def eval(self, env: dict[str, "_Expr"]) -> "_Expr":
        lf = env[self.id]
        ps = [e.eval(env) for e in self.es]
        env = ext_env(env, lf.ids, ps)
        #print(env["x"].v)
        return lf.f.eval(env)
        # TODO fix unintended behavior like
        # f() = x
        # x = 100
        # f() -> 100
        # (could do this by checking the number of ids given matches expected (this may just fix itself when correct typing is added))
    def comp(self, env) -> str: # TODO
        return super().comp(env)

# function definition
class LetFun(_Expr):
    def __init__(self, fid, *args): # given f(x, y) = x + y ...
        self.id = fid # f
        self.ids = [var.id for var in args[:-2]] # x, y
        self.f = args[-2] # x + y
        self.e = args[-1] # ...
    def check_typing(self, env) -> bool:
        return True # TODO (maybe fix this by implementing generic that has .expects_ids which gives the expected types as well)
    def check_binding(self, env) -> bool:
        return self.e.check_binding(ext_env(env, self.ids, ([None] * len(self.ids))))
    def get_eval_type(self, env: dict[str, "_Expr"]) -> int:
        return self.e.get_eval_type(ext_env(env, self.id, self))
    def eval(self, env: dict[str, "_Expr"]) -> "_Expr":
        return self.e.eval(ext_env(env, self.id, self))
    def comp(self, env) -> str: # TODO
        return super().comp(env)

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