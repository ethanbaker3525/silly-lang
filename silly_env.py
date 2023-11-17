from silly_ast import _Expr as Expr

# f(x,y,z) = x + 1 * 3 * y * z + a -> {f:closure([x, y, z], expr(x + 1 * 3 * y * z + a))}

class Closure:
    def __init__(self, ids:list[str], e:Expr, env:"Env"):
        self.ids:list[str] = ids
        self.e:Expr = e
        self.env:"Env" = env
    def bind(self, es:list[Expr]):
        #for i in len(ids):
            #assert self.ids[i] == ids[i]
            #assert len
        #print(self.ids)
        #print(es)
        d = {self.ids[i]: es[i] for i in range(len(es))}
        return self.env.ext(Env(d))

    

class Env:
    def __init__(self, binds:dict[str, Closure]):
        self.binds = binds
    def __str__(self):
        return str(self.binds)
    def lookup(self, ids:str):
        return self.binds[ids]
    def ext(self, env:"Env"):
        #print(self.binds)
        binds = dict(self.binds)
        for xid, e in env.binds.items():
            binds[xid] = e
        return Env(binds)