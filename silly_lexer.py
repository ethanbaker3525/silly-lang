import silly_symbols

def lex_first(raw: str) -> tuple[silly_symbols.Symbol, str]:
    for symbol in silly_symbols.SYMBOLS:
        res = symbol().match(raw)
        if res != None:
            return symbol, res

    raise Exception("lexer error")

def lex_all(raw: str) -> list[silly_symbols.Symbol]:
    lexed = []
    while raw or raw.isspace():
        symbol, raw = lex_first(raw)
        lexed.append(symbol)

    return lexed