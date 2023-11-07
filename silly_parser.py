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
    prog    : expr

    ?expr   : op1               // ops
            | op2
            | if                // conditionals
            | match
            | array             // list like types
            | NUM   -> num      // terminals
            | STR   -> str
            | BOOL  -> bool

    // binary ops
    ?op2    : expr "+"      expr -> add // num ops
            | expr "-"      expr -> sub
            | expr "*"      expr -> mul
            | expr "/"      expr -> div
            | expr "^"      expr -> pow
            | expr "and"    expr -> and // bool ops
            | expr "or"     expr -> or
            | expr "xor"    expr -> xor
            | expr "="      expr -> eq // eq ops
            | expr "!="     expr -> neq
            | expr ">"      expr -> gt
            | expr "<"      expr -> lt
            | expr ">="     expr -> geq
            | expr "<="     expr -> leq

    ?op1    : "-"   expr     -> neg // num ops
            | "not" expr     -> not // bool ops
            | "("   expr ")"

    // list datatypes
    array  : "(" [expr ("," expr)*] ")"           -> vec
            | "[" [expr ("," expr)*] "]"           -> list
            | "{" [expr ("," expr)*] "}"           -> set
            //| "{" [expr ":" expr ("," expr ":" expr)*] "}" -> map

    // conditionals
    if      : "if" expr expr expr
    match   : "match" expr [expr "=>" expr]+

    // terminals
    ID  : /[a-z|A-Z]+[a-z|A-Z|0-9|_]*/ 
    NUM : /-?\d+(\.\d+)?([eE][+-]?\d+)?/
    STR : /".*?(?<!\\)"/
    BOOL: /true|false/
    COMMENT: /#.*/

    %import common.WS
    %ignore WS
    %ignore COMMENT
    '''

    def __init__(self):

        super().__init__(self.__class__.grammar, start="prog")
        self.ast_transformer = ast_utils.create_transformer(silly_ast, silly_ast.ToAst())

    def parse(self, text: str):
        return self.ast_transformer.transform(super().parse(text))
