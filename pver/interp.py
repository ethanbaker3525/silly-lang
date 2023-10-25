import silly_lexer  as lexer
import silly_parser as parser

PROMPT = ":3 "

if __name__ == "__main__":

    raw = input(PROMPT)
    
    while True:
        
        tokens = lexer.lex_all(raw) # str  -> toks (turn raw input into tokens)
        expr = parser.parse(tokens) # toks -> expr (parse tokens into malformed ast)
        expr.rectify()              # expr -> expr (reform ast with correct order of ops)
        expr = expr.eval()          # expr -> expr (evaluate ast and produce a result)
        print(expr)

        raw = input(PROMPT) 