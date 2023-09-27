import re

# general symbol definition, used to define specific symbols

class Symbol:

    re_rep = None

    def __init__(self):
        self.value = None

    def __str__(self):
        rep = type(self).__name__
        if self.value != None:
            rep += ": (" + str(self.value + ")")
        return rep

    def parse_value(raw_val, *args):
        pass

    def match(self, raw_in: str) -> str: # removes symbol from string if it matches
        split = self.re_rep.split(raw_in, maxsplit=1)
        if not split[0] or split[0].isspace(): # symbol does match
            self.parse_value(split[1]) # parsing value if needed
            return split[-1] # returns the rest of the string

# specific symbol definitions, these are used in the lexer

# symbols with values

class SymInt(Symbol):

    re_rep = re.compile("(\d+)")

    def parse_value(self, raw_val):
        self.value = int(raw_val)

class SymFloat(Symbol):

    re_rep = re.compile("(\d+\.\d+)")

    def parse_value(self, raw_val):
        self.value = float(raw_val)

class SymNamespace(Symbol):

    re_rep = re.compile("([a-z|A-Z]+[a-z|A-Z|0-9|_]*)")

    def parse_value(self, raw_val):
        self.value = raw_val

class SymComment(Symbol):

    re_rep = re.compile("#(.*)")

    def parse_value(self, raw_val):
        self.value = raw_val

# symbols with no values

class SymAdd(Symbol):
    re_rep = re.compile("(\+)")

class SymSub(Symbol):
    re_rep = re.compile("(-)")

class SymEqual(Symbol):
    re_rep = re.compile("(=)")

class SymTrue(Symbol):
    re_rep = re.compile("(true)")

class SymFalse(Symbol):
    re_rep = re.compile("(false)")

class SymOpenParen(Symbol):
    re_rep = re.compile("(\()") 

class SymCloseParen(Symbol):
    re_rep = re.compile("(\))")

# const containing all recognized symbols

SYMBOLS = [
    SymComment,
    #SymIf,
    #SymThen,
    #SymElse,
    #SymNot, 
    #SymAnd, 
    #SymOr, 
    SymFloat,
    SymInt,
    SymTrue,
    SymFalse,
    SymAdd,
    SymSub,
    #SymMul,
    #SymDiv,
    #SymMod,
    SymEqual,
    #SymComma,
    #SymDot,
    #Sym1Quote,
    #Sym2Quote,
    SymOpenParen,
    SymCloseParen,
    #SymOpenBracket,
    #SymCloseBracket,
    SymNamespace,

]

"""
class


class Symbols(Enum):

    COMMENT =       re.compile()
    IF =            re.compile("(if)")
    THEN =          re.compile("(then)")
    ELSE =          re.compile("(else)")
    NOT =           re.compile("(not|!)")
    AND =           re.compile("(and|&)")
    OR =            re.compile("(or|\|)")


    ADD =           re.compile("(\+)")

    DIV =           re.compile("(/)")
    MUL =           re.compile("(\*)")
    MOD =           re.compile("(\%)")
    EQUAL =         
    COMMA =         re.compile("(,)")
    DOT =           re.compile("(\.)")
    QUOTE_1 =       re.compile("(')")
    QUOTE_2 =       re.compile("(\")")
    OPEN_PAREN =    
    OPEN_BRAKET =   re.compile("(\[)")
    CLOSE_BRAKET =  re.compile("(\])")


"""