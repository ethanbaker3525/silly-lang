import unittest
import random
from silly_run import comp_run, interp_run
from silly_ast import *
from silly_ast import (
    _Expr as Expr,
    _Lit as Lit,
    _Op2 as Op2,
    _Op1 as Op1, 
    _OpN as OpN,
    _Let as Let)
def run_test(tm, s, v):
    tm(interp_run(s), v)
    tm(comp_run(s), v)

class TestParse(unittest.TestCase):
    pass

def get_expr_subclasses(e=Expr, no_generic=True):
    escs = []
    for e0 in e.__subclasses__():
        if not "._" in str(e0) or not no_generic:
            escs.append(e0)
        escs += get_expr_subclasses(e=e0)
    return escs

def generate_random_expr(es=[Add, Sub, Mul, Div, And, Or, Xor, If], types=[0,1,2], max_lits=10, seed=0): # generate a random VALID expr given the ops
    # generate a valid ast
    random.shuffle(es)
    for e in es:
        match e:
            case Lit():
                e()
            case Op1():
                e()
            case _:
                pass
    
def randomTestOps(ops:list, num_range, cases, num_tests=100, seed=0):
    print(f"seed: {seed}")
    for i in range(num_tests):
        pass

class TestCompInterp(unittest.TestCase):
    
    def testAdd(self):
        run_test(self.assertEqual, "1 + 1", 2)
        run_test(self.assertEqual, "1 + -1", 0)
        run_test(self.assertEqual, "1 + -100", -99)
        run_test(self.assertEqual, "1 + 2 + 3 + -10 + -10", -14)
    
    def testSub(self):
        pass

    def testMul(self):
        pass

    def testDiv(self):
        pass

    def testPow(self):
        pass
        

if __name__ == "__main__":
    generate_random_expr()