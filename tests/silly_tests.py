import unittest

from silly_parser import parse
from silly_interpreter import interp
from silly_compiler import comp

class TestParse(unittest.TestCase):
    def testAdd(self):
        pass

class TestInterp(unittest.TestCase):
    def testAdd(self):
        self.assertEqual(interp(parse("1 + 1")).v, 2)

class TestComp(unittest.TestCase):
    def testAdd(self):
        self.assertEqual(comp(parse("1 + 1")).v, 2)