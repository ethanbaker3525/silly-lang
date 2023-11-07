import pver.silly_parser_old as silly_parser_old

def eval_expr(expr, types=[], env=[]): # expr ast -> expr ast

    #print("EXPR: " + str(expr))

    match expr:

        case []:
            return []

        case [["INT"|"BOOL", _], *rest]:
            return [expr[0]] + rest

        case [["FUNC", "EQUAL"], *rest]:
            match eval_expr(rest, types=types, env=env):

                case [["BOOL", b1], ["BOOL", b2], *rest]:
                    return [["BOOL", (b1 == b2)]] + eval_expr(rest, types=types, env=env)

                case [["INT", i1], ["INT", i2], *rest]:
                    return [["BOOL", (i1 == i2)]] + eval_expr(rest, types=types, env=env)
                
                case _ :
                    return [["ERR", expr]]

        case [["FUNC", "ADD"], *rest]:
            match eval_expr(rest, types=types, env=env):

                case [["INT", val1], ["INT", val2], *rest]:
                    return [["INT", (val1 + val2)]] + eval_expr(rest, types=types, env=env)

                case _ :
                    return [["ERR", expr]]

        case [["FUNC", name], *rest]:

            if name in env:

                return eval_expr(env[name] + rest, types=types, env=env)


            else:

                match eval_expr(rest, types=types, env=env):

                    case [["FUNC", "EQUAL"], *rest]:

                        env[name] = eval_expr(rest, types=types, env=env)
                        return eval_expr(rest, types=types, env=env)
                    
                    case _ :
                        return expr

            
        
        case _ :
            return expr