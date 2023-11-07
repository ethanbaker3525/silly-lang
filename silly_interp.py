from sys import argv

import silly_parser

parser = silly_parser.Parser()

def evaluate(s):
    ast = parser.parse(s)   # ast with ambig typing and ops
    print("ast: " + str(ast))
    print("return type: " + str(ast.t))
    print("ids in scope: " + str(ast.env))
    return ast.eval()       # returning the evaluated value

def res(e):
    print(e)
    print(e.t)
    return e.v

def show_res(res):
    print(res)

if __name__ == '__main__':
    if len(argv) == 1:
        x = input('> ')
        while True:
            show_res(res(evaluate(x)))
            x = input('> ')
    else:
        with open(argv[1], "r") as x:
            show_res(res(evaluate(x.read())))