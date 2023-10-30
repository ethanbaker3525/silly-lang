# imports
from typing import Callable

# Exprs
# generic ast definition
class Expr:

    precedence = -1

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]): # could refactor this to be l and r instead of subs
        self.value  = value  # value is where needed data is stored (eg. integer values, err messages), may need to add more types in the future, or just make your own binary data representations
        self.subs   = subs   # subs is where all sub exprs are stored

    def __str__(self) -> str: 
        rep = str(self.__class__) + ": "
        if self.value != None:
            rep += " [value = " + str(self.value) + "]"
        if self.subs != []:
            rep += " [num_sub_exprs = " + str(len(self.subs)) + "]"
        return rep

    def tree_rep(self, indent=0) -> str: 
        rep = " " * (4*indent) + str(self)
        for sub in self.subs:
                rep += "\n" + sub.tree_rep(indent=(indent+1))
        return rep

    # returns True if self or any subs is an instance of Err, else False
    def has_err(self) -> bool:
        if isinstance(self, Err): # base case
            return True
        for sub in self.subs: # recursive case (will not trigger if no subs)
            if sub.has_err():
                return True
        return False

    # a generic expr cannot be evaluated, must be implemented by children
    def eval(self) -> "Expr":
        return EvalErr(msg="cannot eval generic Expr")

# BinOps
# generic binop definition 
# BinOp ::= <Int> + <Int>
#         | <Int> - <Int>
#         | <Int> * <Int>
#         | <Int> / <Int>
class BinOp(Expr):

    precedence = -1

    op: Callable[[Expr, Expr], Expr] = lambda l, r : EvalErr("cannot eval generic BinOp") # op is the function called when evaluating the l and r exprs, returns an expr
    err_msg: str = "binop" # err_msg is the error message included if evaluating l or r results in an error (a message of "a" will result in a final error message of "eval err, a")

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        assert len(subs) == 2
        super().__init__(subs=subs)
    
    def eval(self) -> Expr:
        l = self.subs[0].eval() # evaluating l and r exprs
        r = self.subs[1].eval()        
        if isinstance(l, Err) or isinstance(r, Err): # error checking and propagation
            return EvalErr(value=self.__class__.err_msg, subs=[l, r])

        return self.__class__.op(l, r) # returns the result of calling op on l and r

# add definition
# <Int> + <Int>
class Add(BinOp):

    precedence = 1
    op = lambda l, r : Int(value = l.value + r.value)
    err_msg = "add"

# sub definition
# <Int> - <Int>
class Sub(BinOp):

    precedence = 1
    op = lambda l, r : Int(value = l.value - r.value)
    err_msg = "sub"

# mul definition
# <Int> * <Int>
class Mul(BinOp):

    precedence = 2
    op = lambda l, r : Int(value = l.value * r.value)
    err_msg = "mul"

# div definition
# <Int> / <Int>
class Div(BinOp):

    precedence = 2
    op = lambda l, r : Int(value = l.value // r.value)
    err_msg = "div"

# pow definition
# <Int> ^ <Int>
class Pow(BinOp):

    precedence = 3
    op = lambda l, r : Int(value = l.value ** r.value)
    err_msg = "pow"

# Lits
# generic lit definition
class Lit(Expr):

    precedence = 0

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value=value)

    def eval(self):
        return self

# integer definition
class Int(Lit):
    pass

# Parens
# parens definition
class Parens(Expr):
    
    precedence = 4

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        assert len(subs) == 1
        super().__init__(subs=subs)

    def eval(self):
        e = self.subs[0].eval()
        if isinstance(e, Err): # error checking and propagation
            return EvalErr(value="parens", subs=[e])
        return e

# Errs
# generic err definition
class Err(Expr):

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value=value, subs=subs)

    def eval(self):
        return self

# ParseErr is used when an error occurs during token parsing
class ParseErr(Err):
    
    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value="parse err, "+value, subs=subs)

# EvalErr is used when an error occurs during ast evaluation
class EvalErr(Err):

    def __init__(self, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value="eval err, "+value, subs=subs)

