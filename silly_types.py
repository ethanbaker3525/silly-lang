UNIT  = 0b0000
BOOL  = 0b0001
INT   = 0b0010
FLOAT = 0b0011
CHAR  = 0b0100
LIST  = 0b1000

NUM = INT

def get_type_str(tn0:int) -> str:
    for ts, tn1 in TYPES.items():
        if tn0 == tn1:
            return ts