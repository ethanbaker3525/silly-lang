# imports
import silly_toks as toks

# takes a string to lex (raw) and returns the first matched token with the rest of the string
def lex_first(raw: str) -> tuple[toks.Tok, str]:
    for tok_class in toks.TOKS: # iter through all recognized tokens
        tok = tok_class() # initalizing new token
        rest = tok.match(raw) # updates tok with value and returns rest on successful match
        if rest != None: # if match is successful
            return tok, rest

    raise Exception("lexer error") # on unsuccessful match raise an error

# takes a string to lex (raw) and returns a list of corresponding tokens
def lex_all(raw: str) -> list[toks.Tok]:
    lexed = [] # list of toks to return
    raw = raw.strip() # removing whitespace from the front and back of raw
    while raw or raw.isspace(): # while the string is not empty
        tok, raw = lex_first(raw) # make the first token and update raw
        lexed.append(tok)

    return lexed