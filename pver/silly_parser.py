import silly_toks   as toks
import silly_lexer  as lexer
import silly_ast    as ast

# is type checking at parse time a stupid idea? would allow for a cfg?

PARSE_GRAMMAR = """
<expr>  ::= (<Expr>)
        |   <>

<op2>

<op1>   ::= <Paren> <(+|-|*|/|^)> <Expr>
        |   <Paren>

<Lit>    ::= int
"""

# returns true if the first tok of ts matches the given tok class
def match_tok(ts: list[toks.Tok], tok_class:toks.Tok):
    if len(ts) > 0 and isinstance(ts[0], tok_class):
        return True
    return False

# returns the class in tok_classes that matches the first tok of ts and None otherwise
def match_toks(ts: list[toks.Tok], tok_classes: list[toks.Tok]):
    for tok_class in tok_classes:
        if match_tok(ts, tok_class):
            return True
    return False


# given a list of tokens returns a well formed ast
def parse(ts) -> ast.Expr:
    e, ts1 = parseExpr(ts) # token list -> malformed ast, token list
    if ts1 == []: # return ast if all toks are consumed
        return e # making malformed tree well formed TODO
    return ast.ParseErr(value="failed to consume all tokens: " + str(ts1)) # otherwise return an error

# parses an expression given a tok list, returns malformed ast
# <Expr>    ::= (<Expr>) 
#           |   <BinOp>
def parseExpr(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    return parseBinOp(ts) # go to state parseBinOp

# parses a binary operation given a tok list, returns malformed ast
# <BinOp>   ::= <Lit> <+|-|*|/> <Expr> (is this correct? this isnt what the well formed ast looks like)
#           |   <Lit>
def parseBinOp(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]: # i will attempt to add precedence to this, and if i cant, i will just make a new state function for higher/ lower precedence ops
    
    # helper functions
    # gets corresponding op from tok_map according to the first tok in ts
    def get_op(ts:list[toks.Tok]):
        tok_map =  {toks.Add:ast.Add,
                    toks.Sub:ast.Sub,
                    toks.Mul:ast.Mul,
                    toks.Div:ast.Div}
        for key, value in tok_map.items():
            if isinstance(ts[0], key):
                return value
        raise Exception("how did this happpen, are you okay?")

    """
    initial:
    

    loop:
    ops =  [add, sub]
    es  =  [1, 2, 1]

    op = ops.pop() -> sub
    e2 = es.pop() -> 1
    e1 = recur

    recur:
    ops =  [add]
    es  =  [1, 2]

    ops =  [add]
    es  =  [1, sub(2 1)]

    """

    # should be able to rewrite this using full recursion
    # shunting yard function that combines expr list and op list with correct precedence
    def sy_combine(es, binops, precedence=0):

        if binops == []:
            print("A")
            print(es)
            print(binops)
            return es[0]

        assert len(binops) + 1 == len(es)

        op = binops.pop()
        print("PRECED")
        print(op.precedence)
        print(precedence)
        print("")
        print(op)
        print("'")
        # if an op on the right has precedence <= the op on its left
        # then it should be evaluated after the other ops (closer to root of ast)
        if op.precedence >= precedence: # L -> R
            print("B")
            print(es)
            print(binops)
            e2 = es.pop() # second expr is last on the stack
            e1 = sy_combine(es, binops, precedence=op.precedence)
            e0 = op(subs=[e1, e2])
            return e0
        # if the op on the right has precedence > the op to its left
        # then it should be evaulated first (closer to the leaves of ast)
        else: # R -> L
            print("C")
            print(es)
            print(binops)
            e2 = es.pop() # second expr is last on the stack
            e1 = es.pop() # first expr is under the second expr
            e0 = op(subs=[e1, e2])
            es.append(e0)
            return sy_combine(es, binops)
        


        """# ops are evaluated from R to L
        print("")
        print("CALLED")
        while binops != []:
            print("")
            print("BINOPS")
            print(binops)
            print("EXPRS")
            print(es)
            op = binops.pop()
            # if an op on the right has precedence <= the op on its left
            # then it should be evaluated after the other ops (closer to root of ast)
            if op.precedence <= precedence: # L -> R
                e2 = es.pop() # second expr is last on the stack
                e1 = sy_combine(es, binops, precedence=op.precedence)
            # if the op on the right has precedence > the op to its left
            # then it should be evaulated first (closer to the leaves of ast)
            else: # R -> L
                e2 = es.pop() # second expr is last on the stack
                e1 = es.pop() # first expr is under the second expr

            e0 = op(subs=[e1, e2])
            es.append(e0)

        
        assert len(es) == 1
        return es[0]"""
        
    e0, ts0 = parseParen(ts) # parsing first expr of binop

    # shunting yard implementation
    # data structs for storing bin ops and exprs
    es:list[ast.Expr] = [e0]
    binops:list[ast.BinOp] = []
    min_precedence = 99
    while match_tok(ts0, (toks.Add, toks.Sub, toks.Mul, toks.Div, toks.Pow)): # while lookahead sees a bin op
        binops.append(get_op(ts0)) # adding the op to the list of binops
        # parsedlit1 add parsedlit2 MUL unparsed
        # lookahead for predictive parsing
        if match_tok(ts0[1:], toks.OpenParen): 
            e0, ts0 = parseParen(ts0[1:]) 
            es.append(e0) 

        elif match_tok(ts0[1:], (toks.Int)): # left recursion (precedence <= max precedence)
            e0, ts0 = parseLit(ts0[1:]) # left recursion (<= precedence) (i dont know if this can be parseLit or has to be parseParen (should work either way due to how paren changes the structure of the ast), i just matched the grammar)
            es.append(e0) # appending parsed expr to es 

        else:
            e0, ts0 = parseExpr(ts0[1:]) # right recursion (> precedence)
            es.append(e0) # appending parsed expr to es 
            break

    #print("TESTING")
    #print(binops)
    #print(es)

    #  3 * 2 + 1
    e0 = sy_combine(es, binops)
    print(e0)

    #print(e0.tree_rep())
    #print(ts0)
    return e0, ts0 # go to state parseParen

# <Paren>   ::= (<Expr>)
#           |   <Lit>
def parseParen(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    if match_tok(ts, toks.OpenParen): # if match on open paren
        e, ts1 = parseExpr(ts[1:]) # parse expr
        if match_tok(ts1, toks.CloseParen):
            return e, ts1[1:]
        return ast.ParseErr(value="unclosed parentheses"), ts1
    return parseLit(ts)

# parses a literal given a tok list, returns well formed ast
# <Lit>     ::= <(int)>
def parseLit(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    if match_tok(ts, toks.Int):
        return ast.Int(value=ts[0].value), ts[1:]
    return ast.ParseErr(value="lit"), ts[1:]


# testing
if __name__ == "__main__":

    ts1 = lexer.lex_all("4 - 3 * 2")
    #ts2 = lexer.lex_all("3 * 2 - 1")

    #print("TOKENS:")
    #print(ts)

    ast1 = parse(ts1)
    #ast2 = parse(ts2)

    #print("MALFORMED AST:")
    print("")
    print(ast1.tree_rep())
    #print(ast2.tree_rep())

    """a, b = ast.split_ast(ast1)
    for e in a:
        print(e)
    print("")
    for e in b:
        print(e)"""

    #ast = ast.reform(ast1)

    #print("WELL FORMED AST:")
    #print(ast.tree_rep())

    print("EVAL:")
    print(ast1.eval())


# len = 5
# idx = 3
# r = 5-3
# l = r-1
# 
# len = 5
# idx = 4
# r = 5-4
