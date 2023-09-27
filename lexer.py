import symbols

def lex_first(raw: str) -> tuple[symbols.Symbol, str]:
    for symbol in symbols.SYMBOLS:
        res = symbol().match(raw)
        if res != None:
            return symbol, res

    raise Exception("lexer error")

def lex_all(raw: str) -> list[symbols.Symbol]:
    lexed = []
    while raw or raw.isspace():
        symbol, raw = lex_first(raw)
        lexed.append(symbol)

    return lexed