import re
from enum import Enum

PROMPT = ":3 "

class Symbol(Enum):

    COMMENT = "#(.*)"
    IF =        "(if)"
    THEN = "(then)"
    ELSE = "(else)"
    NOT = "(not|!)"
    AND = "(and|&)"
    OR = "(or|\|)"
    FLOAT = "(\d+\.\d+)"
    INT = "(\d+)"
    BOOL = "(true|false)"
    ADD = "(\+)"
    SUB = "(-)"
    DIV = "(/)"
    MUL = "(\*)"
    MOD = "(\%)"
    EQUAL = "(=)"
    COMMA =         "(,)"
    DOT =           "(\.)"
    QUOTE_1 =       "(')"
    QUOTE_2 =       "(\")"
    OPEN_PAREN =    "(\()"
    CLOSE_PAREN =   "(\))"
    OPEN_BRAKET =   "(\[)"
    CLOSE_BRAKET =  "(\])"
    NAME =          "([a-z|A-Z]+[a-z|A-Z|0-9|_]*)"


symbols = {

    "COMMENT"      : re.compile("#(.*)"),
    "IF"           : re.compile("(if)"),
    "THEN"         : re.compile("(then)"),
    "ELSE"         : re.compile("(else)"),
    "NOT"          : re.compile("(not|!)"),
    "AND"          : re.compile("(and|&)"),
    "OR"           : re.compile("(or|\|)"),
    "FLOAT"        : re.compile("(\d+\.\d+)"),
    "INT"          : re.compile("(\d+)"),
    "BOOL"         : re.compile("(true|false)"),
    "ADD"          : re.compile("(\+)"),
    "SUB"          : re.compile("(-)"),
    "DIV"          : re.compile("(/)"),
    "MUL"          : re.compile("(\*)"),
    "MOD"          : re.compile("(\%)"),
    "EQUAL"        : re.compile("(=)"),
    "COMMA"        : re.compile("(,)"),
    "DOT"          : re.compile("(\.)"),
    "1_QUOTE"      : re.compile("(')"),
    "2_QUOTE"      : re.compile("(\")"),
    "OPEN_PAREN"   : re.compile("(\()"),
    "CLOSE_PAREN"  : re.compile("(\))"),
    "OPEN_BRAKET"  : re.compile("(\[)"),
    "CLOSE_BRAKET" : re.compile("(\])"),
    "NAME"         : re.compile("([a-z|A-Z]+[a-z|A-Z|0-9|_]*)")

}

def gen_sym_first(raw): # str - > (sym, str)

    for sym, sym_re in symbols.items():
        split = sym_re.split(raw, maxsplit=1)
        #print(split)
        if not split[0] or split[0].isspace():
            return (sym, split[1]), split[-1]

    raise Exception("error generating symbols")

def gen_syms(raw: str) -> list: # str -> sym list

    syms = []
    while raw and not raw.isspace():
        sym, raw = gen_sym_first(raw)
        syms.append(sym)
    return syms

def parse_syms(syms, expr_ast, exprs=0): # syms list -> expr ast

    print(syms)
    print(expr_ast)
    print(exprs)

    match syms:

        case []:            # base case
            return expr_ast

        case [["INT", val], *rest]:  # primitives
            return parse_syms(rest, expr_ast + [["INT", int(val)]], exprs=exprs+1)
        case [["FLOAT", val], *rest]:
            return parse_syms(rest, expr_ast + [["FLOAT", float(val)]] )
        case [["BOOL", val], *rest]:
            return parse_syms(rest, expr_ast + [["BOOL", val == "true"]])

        case [["OPEN_PAREN", _], *rest]:
            return expr_ast

        case [["ADD", _], *rest]:    # int ops

            return expr_ast[:exprs-1] + parse_syms(rest, [["FUNC", "ADD"]] + expr_ast[exprs-1:], exprs=exprs)
 ### ISSUE WITH + 1 1 or 1 + 2 + 3 + 4
        case [["EQUAL", _], *rest]:    # int ops
            return expr_ast[exprs:] + [["FUNC", "EQUAL"]] + parse_syms(rest, expr_ast[:exprs])

        case [["NAME", name], *rest]:    # int ops
            return parse_syms(rest, expr_ast + [["FUNC", name]])
            
        case _ :
            raise Exception("parse_syms")

def eval_expr(expr, types=[], env=[]): # expr ast -> expr ast

    #print("EXPR: " + str(expr))

    match expr:

        case []:
            return []

        case [["INT"|"BOOL", _], *rest]:
            return [expr[0]] + rest

        case [["FUNC", "EQUAL"], *rest]:
            match eval_expr(rest, types=types, env=env):

                case [["BOOL", b1], ["BOOL", b2], *rest]:
                    return [["BOOL", (b1 == b2)]] + eval_expr(rest, types=types, env=env)

                case [["INT", i1], ["INT", i2], *rest]:
                    return [["BOOL", (i1 == i2)]] + eval_expr(rest, types=types, env=env)
                
                case _ :
                    return [["ERR", expr]]

        case [["FUNC", "ADD"], *rest]:
            match eval_expr(rest, types=types, env=env):

                case [["INT", val1], ["INT", val2], *rest]:
                    return [["INT", (val1 + val2)]] + eval_expr(rest, types=types, env=env)

                case _ :
                    return [["ERR", expr]]

        case [["FUNC", name], *rest]:

            if name in env:

                return eval_expr(env[name] + rest, types=types, env=env)


            else:

                match eval_expr(rest, types=types, env=env):

                    case [["FUNC", "EQUAL"], *rest]:

                        env[name] = eval_expr(rest, types=types, env=env)
                        return eval_expr(rest, types=types, env=env)
                    
                    case _ :
                        return expr

            
        
        case _ :
            return expr

def show_res(expr):
    for e in expr:
        print("= " + str(e[1]) + " (type = " + e[0] + ")")

if __name__ == "__main__":

    raw = input(PROMPT)
    
    while True:
        
        syms = gen_syms(raw) # str -> syms
        print(syms)
        #expr = parse_syms(syms, []) # syms -> expr
        #print(expr)
        #res = eval_expr(expr, env={"a":[["INT", 1]]})
        #print(res)
        #show_res(res)

        raw = input(PROMPT)
        
        

