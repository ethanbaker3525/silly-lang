import lexer
import parser

PROMPT = ":3 "

if __name__ == "__main__":

    raw = input(PROMPT)
    
    while True:
        
        syms = lexer.lex_all(raw) # str -> syms
        print(syms)
        #expr = parse_syms(syms, []) # syms -> expr
        #print(expr)
        #res = eval_expr(expr, env={"a":[["INT", 1]]})
        #print(res)
        #show_res(res)

        raw = input(PROMPT) 