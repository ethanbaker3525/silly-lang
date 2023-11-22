from sys import exit as sysexit
from lark.exceptions import *

class SillyException(Exception): pass

class CompErr(SillyException): pass

class InterpErr(SillyException): pass

class ParseErr(SillyException): pass

def err(e:Exception, text:str):
    match e:
        case UnexpectedInput():
            _parse_err(e, text)
        
def _parse_err(e:UnexpectedInput, text:str):
    match e:
        case UnexpectedEOF():
            l, c = _wrap_l_c_count(e.line, e.column, text)
        case _:
            l = e.line
            c = e.column
    _print_parse_err(l, c, e.get_context(text))
    sysexit(1)

def _wrap_l_c_count(l, c, text, offset=1):
    lines = text.split("\n")
    newl = len(lines) + l + offset
    newc = len(lines[l]) + c + offset
    return newl, newc

def _print_parse_err(l, c, context):
    m = "line {l} column {c}\n{context}".format(l=l, c=c, context=context)
    _print_err("parse", m)

def _print_err(t:str, m:str):
    print("{t} err\n{m}".format(t=t, m=m))