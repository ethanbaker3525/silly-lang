# imports
from typing import Callable
from sys    import maxsize
from copy   import copy, deepcopy
from enum   import Enum

DEFAULT_PRECEDENCE = {
    "lit"   : 0,
    "err"   : 6,
    "paren" : 4,
    "pow"   : 3,
    "mul"   : 2,
    "add"   : 1
}

# Exprs
# generic ast definition
class Expr:

    def __init__(self, preced:int=0, value:(int|str)=None, subs:list["Expr"]=[]):
        self.preced = preced # the precedence of the expression, higher -> evaluate earlier
        self.value  = value  # value is where needed data is stored (eg. integer values, err messages), may need to add more types in the future, or just make your own binary data representations
        self.subs   = subs   # subs is where all sub exprs are stored

    def __lt__(self, other):
        return self.preced < other.preced

    def __le__(self, other):
        return self.preced <= other.preced

    def __eq__(self, other):
        return self.preced == other.preced

    def __ne__(self, other):
        return self.preced != other.preced

    def __gt__(self, other):
        return self.preced > other.preced

    def __ge__(self, other):
        return self.preced >= other.preced

    def __str__(self) -> str: 
        rep = str(self.__class__) + ": [precedence = " + str(self.preced) + "]" # sub exprs are indented by 4 spaces
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

    op: Callable[[Expr, Expr], Expr] = lambda l, r : EvalErr("cannot eval generic BinOp") # op is the function called when evaluating the l and r exprs, returns an expr
    err_msg: str = "binop" # err_msg is the error message included if evaluating l or r results in an error (a message of "a" will result in a final error message of "eval err, a")

    def __init__(self, preced:int=0, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(preced=preced, subs=subs)
        self.preced = self.__class__.default_preced
    
    def eval(self) -> Expr:
        l = self.subs[0].eval() # evaluating l and r exprs
        r = self.subs[1].eval()        
        if isinstance(l, Err) or isinstance(r, Err): # error checking and propagation
            return EvalErr(value=self.__class__.err_msg, subs=[l, r])

        return self.__class__.op(l, r) # returns the result of calling op on l and r

# add definition
# <Int> + <Int>
class Add(BinOp):

    default_preced = DEFAULT_PRECEDENCE["add"]
    op = lambda l, r : Int(value = l.value + r.value)
    err_msg = "add"

# sub definition
# <Int> - <Int>
class Sub(BinOp):

    default_preced = DEFAULT_PRECEDENCE["add"]
    op = lambda l, r : Int(value = l.value - r.value)
    err_msg = "sub"

# mul definition
# <Int> * <Int>
class Mul(BinOp):

    default_preced = DEFAULT_PRECEDENCE["mul"]
    op = lambda l, r : Int(value = l.value * r.value)
    err_msg = "mul"

# div definition
# <Int> / <Int>
class Div(BinOp):

    default_preced = DEFAULT_PRECEDENCE["mul"]
    op = lambda l, r : Int(value = l.value // r.value)
    err_msg = "div"

# pow definition
# <Int> ^ <Int>
class Pow(BinOp):

    default_preced = DEFAULT_PRECEDENCE["pow"]
    op = lambda l, r : Int(value = l.value ** r.value)
    err_msg = "pow"

# Lits
# generic lit definition
class Lit(Expr):

    default_preced = DEFAULT_PRECEDENCE["lit"]

    def __init__(self, preced:int=default_preced, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(preced=preced, value=value)

    def eval(self):
        return self

# integer definition
class Int(Lit):
    pass

# Errs
# generic err definition
class Err(Expr):

    default_preced = DEFAULT_PRECEDENCE["err"]

    def __init__(self, preced:int=0, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value=value, subs=subs)

    def eval(self):
        return self

# ParseErr is used when an error occurs during token parsing
class ParseErr(Err):
    
    def __init__(self, preced:int=0, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value="parse err, "+value, subs=subs)

# EvalErr is used when an error occurs during ast evaluation
class EvalErr(Err):

    def __init__(self, preced:int=0, value:(int|str)=None, subs:list["Expr"]=[]):
        super().__init__(value="eval err, "+value, subs=subs)

# functions for reforming malformed asts
# takes a marformed ast and returns the depth first traversal of the ast in list form (all subs are also removed)
def dft_split(ast: Expr) -> list[Expr]:
    lst = []
    for sub in ast.subs:
        lst += dft_split(sub)
    ast.subs = []
    return lst + [ast]

# takes a list that is a depth first traversal of a malformed ast and stitches the list into a well formed ast
def dft_stitch(lst: list[Expr]) -> Expr:
    lst_len = len(lst)
    assert lst_len % 2 == 1 # list must be odd length
    print("lst: " + str(lst))

    # base case
    if len(lst) == 1: 
        return lst[0]

    # recursive case
    i = lst_len - 1
    max_i = i
    max_op = lst[i]
    while i > lst_len//2:
        if lst[i] > max_op:
            max_op = lst[i]
            max_i = i
        i -= 1
    r_i = lst_len - max_i
    max_op.subs = [lst[r_i-1], lst[r_i]]
    max_op.preced = -1
    rest_lst = lst[:r_i-1] + lst[r_i+1:max_i] + lst[max_i+1:]
    print("rest:" + str(rest_lst))
    return dft_stitch([max_op] + rest_lst) # adds the expr to the front of the list and continues
    
    
    
    


# one pass over expr tree to fix precedence issues (instead of making a ll1 parser)
# lower precedence exprs must be lower (closer to leafs) on the tree
# equal precedence exprs must have their precedence reversed
def reform(ast: Expr):

    lst = dft_split(ast)
    print(lst)
    #return dft_stitch(lst)
    return ast


    """if ast.subs != []:
        subs = []
        for sub in ast.subs:
            subs.append(rectify(sub))
        sub = min(subs)
        if ast > sub:
            return sub.__class__()"""

    
    



    """print("rectifying!")
    subs = []
    for sub in self.subs: # recursive case
        subs.append(sub.rectify())
    
    for sub in subs:
        print(str(self.preced) + " " + str(sub.preced))
        # if the child parent precedence is wrong
        # swap the parent with the min of the children
        if self > sub:
            min(subs)
            
        # if the child (e2) and parent (p) have equal precedence
        # build left expr tree with dfs (l then r then root)
        elif self == sub:  
            print("not ready!") 
    return self"""