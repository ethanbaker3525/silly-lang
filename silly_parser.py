import sys
from typing import List
from dataclasses import dataclass

from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

import silly_ast

class Parser(Lark):

    grammar = r'''
    // to add
    // match
    // type definition
    // type annotations

    // top level program
        prog    : expr

        ?expr   : let
                | if
                | op

        ?let    : ID "=" expr expr -> let_var
                | ID "(" (expr ("," expr)*)? ")" "=" expr expr -> let_fun

        ?if     : "if" expr "then" expr "else" expr -> if

        ?op     : and
        ?and    : and "and" not -> and
                | and "or"  not -> or
                | and "xor" not -> xor
                | not
        ?not    : "not" eq -> not
                | eq
        ?eq     : eq "="  add -> eq
                | eq "!=" add -> neq
                | eq ">"  add -> gr
                | eq ">=" add -> geq
                | eq "<"  add -> lt
                | eq "<=" add -> leq
                | add
        ?add    : add "+" mul -> add
                | add "-" mul -> sub
                | "-" add     -> neg
                | mul
        ?mul    : mul "*" exp -> mul
                | mul "/" exp -> div
                | exp
        ?exp    : exp "^" atom -> exp
                | atom
        ?atom   : "(" expr ")"
                | expr
                | ID "(" (expr ("," expr)*)? ")" -> fun
                | ID -> var
                | NUM -> num
                | STR -> str
                | BOOL -> bool

        ID      : /[a-z|A-Z]+[a-z|A-Z|0-9|_]*/ 
        NUM     : /-?\d+(\.\d+)?([eE][+-]?\d+)?/
        STR     : /".*?(?<!\\)"/
        BOOL.1  : /true|false/
        COMMENT : /#.*/

        %import common.WS
        %ignore WS
        %ignore COMMENT
    '''

    def __init__(self):

        super().__init__(self.__class__.grammar, start="prog") # , parser="lalr"
        self.ast_transformer = ast_utils.create_transformer(silly_ast, silly_ast.ToAst())

    def parse(self, text: str):
        self.p = super().parse(text)

    def to_ast(self):
        return self.ast_transformer.transform(self.p)

if __name__ == "__main__":

        # the problem:
        # if x = 1 ... 
        # is parsed as a let assignment instead of a bool eq 
        # because there are more exprs after it.
        # solution ideas:
        # 1. parse all = ambiguously and then figure it out during 
        # transformer step
        # 
        #

        p = Parser()
        p.parse("""
                not true
                """)
        print(p.p.pretty())
