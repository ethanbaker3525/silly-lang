import unittest

from silly_run import comp_run, interp_run

def run_test(test_method, s, v):
    test_method(interp_run(s), v)
    test_method(comp_run(s), v)

class TestParse(unittest.TestCase):
    pass

class TestCompInterp(unittest.TestCase):
    
    def testAdd(self):
        run_test(self.assertEqual, "1 + 1", 2)
        run_test(self.assertEqual, "1 + -1", 0)
        run_test(self.assertEqual, "1 + -100", -99)
        run_test(self.assertEqual, "1 + 2 + 3 + -10 + -10", -14)
        

