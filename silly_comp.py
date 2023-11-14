from sys import argv
import silly_parser
from silly_utils import get_type_str, err

EXT = "silly"
TEMPLATE = """global _entry
global _type
default rel

section .data
_type: db {tn} ; eval type is {ts}

section .text
_entry:{asm}
    ret"""

def compile(e):
    if not e.check_typing():
        err("bad typing")
    asm = e.comp([])
    tn = e.get_eval_type()
    return TEMPLATE.format(asm=asm, tn=tn, ts=get_type_str(tn))

if __name__ == "__main__":
    if len(argv) == 2: # if not one cmdline arg do nothing
        if argv[1][-len(EXT):] == EXT: # if is .silly file
            fname_asm = None # then we dont want to make an asm
            fname_silly = argv[1]
        else:
            fname_asm = argv[1]
            fname_silly = argv[1].split("/")[2][:-len("asm")] + EXT
        with open(fname_silly, "r") as f:
            p = silly_parser.Parser()
            p.parse(f.read())
            #sprint(p.p.pretty())
            ast = p.to_ast()
            asm = compile(ast)
        if fname_asm == None:
            print(asm) # printing asm instead of making .asm file
        else:
            with open(fname_asm, "w") as file:
                file.write(asm)


    


