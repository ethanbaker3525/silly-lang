import silly_toks   as toks
import silly_lexer  as lexer
import silly_ast    as ast

# is type checking at parse time a stupid idea? would allow for a cfg?

GRAMMAR = """
<Expr>  ::= (<Expr>) 
        |   <BinOp>

<BinOp> ::= <Lit> <(+|-|*|/|^)> <Expr>
        |   <Lit>

<Lit>    ::= <(int)>
"""

# returns true if the first tok of ts matches the given tok class
def match_tok(ts: list[toks.Tok], tok_class:toks.Tok):
    if len(ts) > 0 and type(ts[0]) == tok_class:
        return True
    return False

# returns the class in tok_classes that matches the first tok of ts and None otherwise
def match_toks(ts: list[toks.Tok], tok_classes: list[toks.Tok]):
    for tok_class in tok_classes:
        if match_tok(ts, tok_class):
            return tok_class
    return None # not neccecary, just for readability

# given a list of tokens returns a well formed ast
def parse(ts) -> ast.Expr:
    e, ts1 = parseExpr(ts) # token list -> malformed ast, token list
    if ts1 == []: # return ast if all toks are consumed
        return e # making malformed tree well formed TODO
    return ast.ParseErr(value="failed to consume all tokens: " + str(ts1)) # otherwise return an error

# parses an expression given a tok list, returns malformed ast
# <Expr> ::= (<Expr>) 
#          | <BinOp>
def parseExpr(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    return parseBinOp(ts) # go to state parseBinOp

# parses a binary operation given a tok list, returns malformed ast
# <BinOp> ::= <Lit> <+|-|*|/> <Expr>
#           | <Lit>
def parseBinOp(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    tok_ast_map =  {toks.Add:ast.Add,
                    toks.Sub:ast.Sub,
                    toks.Mul:ast.Mul,
                    toks.Div:ast.Div,
                    toks.Pow:ast.Pow}
    e1, ts1 = parseParen(ts) # parsing literal

    tc = match_toks(ts1, tok_ast_map.keys()) # gets the tok class that is matched
    if tc != None: # if the match is successful then continue in this state 
        e2, ts2 = parseExpr(ts1[1:]) # parsing expr (ts1[1:] consumes the +|-|*|/ token)
        return tok_ast_map[tc](subs=[e1, e2]), ts2 # returning the appropriate binop (the one that was matched)

    return e1, ts1 # go to state parseLit

# parses a literal given a tok list, returns well formed ast
# <Lit> ::= <(int)>
def parseLit(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    if match_tok(ts, toks.Int):
        return ast.Int(value=ts[0].value), ts[1:]
    


def parseParen(ts: list[toks.Tok]) -> tuple[ast.Expr, list[toks.Tok]]:
    if match_tok(ts, toks.OpenParen): # if match on open paren
        e, ts1 = parseExpr(ts[1:]) # parse expr
        if match_tok(ts1, toks.CloseParen):
            e.preced = ast.DEFAULT_PRECEDENCE["paren"]
            return e, ts1[1:]
        return ast.ParseErr(value="unclosed parentheses"), ts1
    
    return ast.ParseErr(value="lit"), ts[1:]

# testing
if __name__ == "__main__":

    ts1 = lexer.lex_all("(3 * 2) - 1")
    ts2 = lexer.lex_all("3 * 2 - 1")

    #print("TOKENS:")
    #print(ts)

    ast1 = parse(ts1)
    ast2 = parse(ts2)

    #print("MALFORMED AST:")
    print(ast1.tree_rep())
    print(ast2.tree_rep())

    #wf_ast = ast.reform(mf_ast)

    #print("WELL FORMED AST:")
    #print(wf_ast.tree_rep())

    #print("EVAL:")
    #print(wf_ast.eval())


# len = 5
# idx = 3
# r = 5-3
# l = r-1
# 
# len = 5
# idx = 4
# r = 5-4
