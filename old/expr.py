types = ["INT", "BOOL", "FUNC"]
env = { 
        "x":                        # name
        [
            [],                     # in types
            ["INT"],                # out type
            lambda: []               # evaluation function
        ]
    }  

def evaluate(types, env, expr):

    match expr:

        case []:
            return []

        case [["INT"|"BOOL", value], *rest]:
            return [expr[0]] + evaluate(types, env, rest)

        case [["FUNC", "INT_EQUAL"], *rest]:
            match evaluate(types, env, rest):

                case [["BOOL", b1], ["BOOL", b2], *rest]:
                    return [["BOOL", (b1 == b2)]] + evaluate(types, env, rest)
                
                case _ :
                    return ["ERR", "error with func ="]

        case [["FUNC", "INT_ADD"], *rest]:
            match evaluate(types, env, rest):

                case [["INT", val1], ["INT", val2], *rest]:
                    return [["INT", (val1 + val2)]] + evaluate(types, env, rest)

                case _ :
                    return ["ERR", "error with func +"]

    
if __name__ == "__main__":

    # 1 = 2 -> false
    e = [["FUNC", "INT_ADD"], ["FUNC", "INT_ADD"], ["INT", 1], ["INT", 4], ["INT", 2], ["INT", 1]] # -> ["BOOL", False]

    print(evaluate(types, env, e))

    #print(e[1:])




