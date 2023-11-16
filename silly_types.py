TYPES = {
    "num"  : 0,
    "int"  : 0,
    "bool" : 1,
    "char" : 2,
    "str"  : 2
}

def get_type_str(tn0:int) -> str:
    for ts, tn1 in TYPES.items():
        if tn0 == tn1:
            return ts