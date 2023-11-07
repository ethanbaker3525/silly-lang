

class Expr:

    name = "generic expr"

    def __init__(self, v=None, es:list["Expr"]=[]): # could refactor this to be l and r instead of s
        self.v  = v   # value is where needed data is stored (eg. integer values, err messages), may need to add more types in the future, or just make your own binary data representations
        self.es = es  # s is where all sub exprs are stored

    def __str__(self) -> str: 
        rep = str(self.__class__) + ": "
        if self.v != None:
            rep += " [value = " + str(self.v) + "]"
        if self.es != []:
            rep += " [num_sub_exprs = " + str(len(self.es)) + "]"
        return rep

    def tree_rep(self, indent=0) -> str: 
        rep = " " * (4*indent) + str(self)
        for sub in self.es:
                rep += "\n" + sub.tree_rep(indent=(indent+1))
        return rep

    def has_err(self) -> bool: # returns True if self or any s is an instance of Err, else False
        if isinstance(self, Err): # base case
            return True
        for sub in self.es:
            if sub.has_err():
                return True
        return False

    def eval(self) -> "Expr": # a generic expr cannot be evaluated, must be implemented by children
        return EvalErr("cant eval generic expr", self.es)

class Op(Expr):

    name = "generic op"
    op = lambda vs: EvalErr("cant eval generic op") # op is the function called when evaluating the l and r exprs, returns an expr

    def eval(self) -> Expr:
        evs = [e.eval() for e in self.es]
        e = self.__class__.op(evs)
        if e.has_err():
            return EvalErr(e.v ,self.es)
        return e

class Add(Op):

    name = "+"
    op = lambda es: Int(es[0].v + es[1].v)

class Sub(Op):

    name = "-"
    op = lambda es: Int(es[0].v - es[1].v)

class Mul(Op):

    name = "*"
    op = lambda es: Int(es[0].v * es[1].v)

class Div(Op):

    name = "/"
    op = lambda es: Int(es[0].v / es[1].v)

class Pow(Op):

    name = "^"
    op = lambda es: Int(es[0].v ** es[1].v)

class Neg(Op):

    name = "-()"
    op = lambda es: Int(0 - es[0].v)

class Paren(Op):

    name = "()"
    op = lambda es: es[0]

class Lit(Expr):

    name = "generic lit"

    def eval(self):
        return self

class Int(Lit):

    name = "int"

class Float(Lit):

    name = "float"

class Bool(Lit):

    name = "bool"

class Err(Expr):

    name = "err"

    def __init__(self, v:str=name, es:list["Expr"]=[]):
        super().__init__(v=v, es=es)

    def eval(self):
        return self

    def trace(self) -> str:
        pass

class ParseErr(Err):

    name = "parse err"

    def __init__(self, v:str=name, es:list["Expr"]=[]):
        super().__init__(v, es)

class EvalErr(Err):

    name = "eval err"

    def __init__(self, v:str=name, es:list["Expr"]=[]):
        super().__init__(v, es)

