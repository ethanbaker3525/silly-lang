from sys import argv

import silly_parser

p = silly_parser.Parser()

def evaluate(s):
    p.parse(s)
    #print(p.p.pretty())
    ast = p.to_ast()
    #print("ast: " + str(ast))
    #print("return type: " + str(ast.t))
    #print("ids in scope: " + str(ast.env))
    env = {}
    x = ast.eval(env)  
    #print(env["x"].v)
    return x     # returning the evaluated value

def res(e):
    #print(e)
    #print(e.t)
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