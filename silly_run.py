import sys
import subprocess
from pathlib import Path
from shutil import rmtree


from silly_parser import parse
from silly_comp import comp
from silly_interp import interp
from silly_utils import *

def comp_main_o(main_c_path, main_o_path, cc="gcc", cc_flags=["-elf", "-c", "-o"]):
    subprocess.run([cc, *cc_flags, main_o_path, main_c_path])

def comp_o(asm_path, asm_o_path, ac="nasm", ac_flags=["-f", "elf64"], ac_o_flag="-o"):
    subprocess.run([ac, *ac_flags, asm_path, ac_o_flag, asm_o_path])

def comp_bin(asm_o_path, main_o_path, bin_path, cc="gcc", cc_o_flag="-o"):
    subprocess.run([cc, asm_o_path, main_o_path, cc_o_flag, bin_path])

def run_bin(bin_path):
    x = subprocess.run(bin_path, capture_output=True)
    return str(x.stdout, encoding="utf-8")[:-1]

def comp_run_str(s:str, main_c_path=Path("main.c"), build_path=Path("./.silly"), name="temp", rm_after_use=True):
    # getting paths
    build_path.mkdir(parents=True, exist_ok=True)
    asm_path = build_path / Path(name + ".asm")
    main_o_path = build_path / Path("main.o")
    asm_o_path = build_path / Path(name + ".o")
    bin_path = build_path / Path(name)
    # building bin
    ast = parse(s) # parsing str to ast
    asm = comp(ast) # getting asm str
    write_prog_file(asm, asm_path) # writing .asm
    comp_main_o(main_c_path, main_o_path)
    comp_o(asm_path, asm_o_path)
    comp_bin(asm_o_path, main_o_path, bin_path)
    # running bin
    result = run_bin(bin_path)
    if rm_after_use: # removing build
        rmtree(build_path)
    return result

def comp_run(s):
    return str_to_val(comp_run_str(s))

def interp_run_str(s:str) -> str:
    ast = parse(s)
    return lit_to_str(interp(ast))

def interp_run(s):
    ast = parse(s)
    return lit_to_val(interp(ast))

def main(args, fp):
    path = Path(fp)
    with open(path, "r") as file:
        s = file.read()
    if "-i" in args or "--interp" in args:
        res = interp_run_str(s)
    elif "-c" in args or "--comp" in args:
        if "-s" in args or "--save" in args:
            res = comp_run_str(s, rm_after_use=False)
        else:
            res = comp_run_str(s, rm_after_use=True)
    else:
        print("include args")
        sys.exit(1)
    print(res)

if __name__ == "__main__":
    main(sys.argv[1:-1], sys.argv[-1])