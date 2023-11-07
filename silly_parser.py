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

        ?expr : numop2
                | boolop2

        ?numop2.1 : add

        ?add    : mul
                | add "+" expr -> add
                | add "-" expr -> sub
        ?mul    : exp
                | mul "*" expr -> mul
                | mul "/" expr -> div
        ?exp    : term
                | exp "^" expr -> div

        ?boolop2: and

        ?and    : term
                | and "and" expr

        ?op1    : neg
                | not

        ?neg    : "-" term
                | "-" expr

        ?not    : "not" expr

        ?term   : NUM   -> num
                | STR   -> str
                | BOOL  -> bool
                | ID    -> id     
                | "(" expr ")"
  




        // terminals
        NUM: /-?\d+(\.\d+)?([eE][+-]?\d+)?/
        STR: /".*?(?<!\\)"/
        BOOL: /true|false/
        ID  : /[a-z|A-Z]+[a-z|A-Z|0-9|_]*/ 
        COMMENT: /#.*/

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
        #return self.ast_transformer.transform(p)
