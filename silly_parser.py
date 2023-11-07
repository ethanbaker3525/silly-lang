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
    // functions
    // function definition
    // type definition
    // type annotations

    // top level program
        prog    : (expr)*

        ?expr   : if
                | match
                | op

        ?if     : "if" expr "then"? expr "else"? expr

        ?match  : "match" expr (expr "=>" expr)+

        ?op     : eq
        ?eq     : not
                | (eq | ID) "=" expr -> bool_eq
                | "let"? ID "=" expr ("in"? expr)+ -> let_eq
        ?not    : and
                | "not" expr -> not
        ?and    : or
                | and "and" expr
        ?or     : add
                | and "or" expr
        ?add    : mul
                | add "+" expr -> add
                | add "-" expr -> sub
                | "-" expr -> neg
        ?mul    : exp
                | mul "*" expr -> mul
                | mul "/" expr -> div
        ?exp    : paren
                | exp "^" expr -> exp
        ?paren  : fcall
                | "(" expr ")"
        ?fcall  : atom
                | ID "(" expr? ("," expr)* ")" -> fcall
        ?atom   : ID -> id
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

        super().__init__(self.__class__.grammar, start="prog", parser="lalr") # 
        self.ast_transformer = ast_utils.create_transformer(silly_ast, silly_ast.ToAst())

    def parse(self, text: str):
        p = super().parse(text)
        print(p.pretty())
        return self.ast_transformer.transform(p)
