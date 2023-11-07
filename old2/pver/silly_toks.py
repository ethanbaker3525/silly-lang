import re

# generic token definition
class Tok:

    re_rep = None

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        rep = type(self).__name__
        if self.value != None:
            rep += ":(" + str(self.value) + ")"
        return rep

    # implemented by children, updates value given raw_val
    def parse_value(raw_val: str, *args):
        pass

    # takes a string of potential tokens (raw), if the first potential token matches self
    # return the rest of raw and update value, otherwise return None
    def match(self, raw: str) -> str: 
        # splits the string based on the given regex
        # split[0] is matching token in raw, split[1] is the rest of raw
        split = self.re_rep.split(raw, maxsplit=1) 
        if not split[0] or split[0].isspace(): # if tok does match
            self.parse_value(split[1]) # parsing value if needed
            return split[-1] # returns the rest of the string

# specific token definitions
# tokens with values
class Int(Tok):
    
    re_rep = re.compile("(-?\d+)")
    def parse_value(self, raw_val):
        self.value = int(raw_val)

class Float(Tok):
    re_rep = re.compile("(-?\d+\.\d+)")
    def parse_value(self, raw_val):
        self.value = float(raw_val)

class ID(Tok):
    re_rep = re.compile("([a-z|A-Z]+[a-z|A-Z|0-9|_]*)")
    def parse_value(self, raw_val):
        self.value = raw_val

class Comment(Tok):
    re_rep = re.compile("#(.*)")
    def parse_value(self, raw_val):
        self.value = raw_val

# tokens without values
class Add(Tok):
    re_rep = re.compile("(\+)")

class Sub(Tok):
    re_rep = re.compile("(-)")

class Mul(Tok):
    re_rep = re.compile("(\*)")

class Div(Tok):
    re_rep = re.compile("(/)")

class Pow(Tok):
    re_rep = re.compile("(\^)")

class Equal(Tok):
    re_rep = re.compile("(=)")

class BoolTrue(Tok):
    re_rep = re.compile("(true)")

class BoolFalse(Tok):
    re_rep = re.compile("(false)")

class OpenParen(Tok):
    re_rep = re.compile("(\()") 

class CloseParen(Tok):
    re_rep = re.compile("(\))")

class EOI(Tok):
    re_rep = None

# list of all recognized tokens
# list order is equivalent to the priority with wich tokens are lexed
# eg. 1.2 will be lexed as a float not int dot int because float is lexed before int
TOKS = [
    Comment,
    #SymIf,
    #SymThen,
    #SymElse,
    #SymNot, 
    #SymAnd, 
    #SymOr, 
    Float,
    Int,
    BoolTrue,
    BoolFalse,
    Add,
    Sub,
    Mul,
    Div,
    Pow,
    #SymMod,
    Equal,
    #SymComma,
    #SymDot,
    #Quote1,
    #Quote2,
    OpenParen,
    CloseParen,
    #SymOpenBracket,
    #SymCloseBracket,
    ID,
    EOI
]