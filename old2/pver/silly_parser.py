import silly_toks   as toks
import silly_lexer  as lexer
import silly_ast    as ast

# is type checking at parse time a stupid idea? would allow for a cfg?

PARSE_GRAMMAR = """

<exprs> ::= <expr> <expr> <expr>...

<expr>  ::= <expr> <op2> <expr>
        |   <>

<op2>   ::= <expr> ^ <expr>
        |   <expr> * <expr>
        |   <expr> / <expr>
        |   <expr> + <expr>
        |   <expr> - <expr>

<op1>   ::= (   <expr>)
        |   -   <expr>
        |   not <expr>

<lit>   ::= int 
        |   float
        |   bool
"""

def lookahead(ts, i=0):
    return type(ts[i])

# returns true if the first tok of ts matches the given tok class
def match_tok(ts: list[toks.Tok], t:toks.Tok):
    if ts == [] and issubclass(lookahead(ts), t):
        return True
    return False

# returns the class in tok_classes that matches the first tok of ts and None otherwise
def match_toks(ts: list[toks.Tok], tok_classes: list[toks.Tok]):
    for tok_class in tok_classes:
        if match_tok(ts, tok_class):
            return True
    return False

def parse(ts: list[toks.Tok]) -> ast.Expr: 
    ts, e = parse_expr(ts)
    if ts == []:
        return e
    print(ts)
    return ast.ParseErr("some tokens remaining", [e])

def parse_expr(ts: list[toks.Tok]) -> tuple[list[toks.Tok], ast.Expr]:
    return parse_op2(ts)

def parse_op2(ts: list[toks.Tok]) -> tuple[list[toks.Tok], ast.Expr]:
    ts, e = parse_op1(ts) # parsing first expr of binop (THIS SHOULD BE LAST VALID PRECEDENCE OP, DO SHUNTING YARD)
    if lookahead(ts) == toks.Add | toks.Sub | toks.Mul | toks.Div | toks.Pow:
        pass

    return ts, e

def parse_op1(ts: list[toks.Tok]) -> tuple[list[toks.Tok], ast.Expr]:
    if lookahead(ts) == toks.OpenParen:
        ts, e = parse_expr(ts[1:])
        if lookahead(ts) == toks.CloseParen:
            return ts[1:], ast.Paren(None, [e])
        return ts, ast.ParseErr("no matching close paren")
    return parse_lit(ts)

def parse_lit(ts: list[toks.Tok]) -> tuple[list[toks.Tok], ast.Expr]:
    if lookahead(ts) == toks.Int: # parsing ints
        return ts[1:], ast.Int(ts[0].value)
    if lookahead(ts) == toks.Float: # parsing floats
        return ts[1:], ast.Float(ts[0].value)
    if lookahead(ts) == toks.BoolTrue: # parsing bools
        return ts[1:], ast.Bool(True)
    if lookahead(ts) == toks.BoolFalse:
        return ts[1:], ast.Bool(False)
    return ts, ast.ParseErr("lit") # no matched literal so err


# testing
if __name__ == "__main__":

    ts1 = lexer.lex_all("(12)")
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