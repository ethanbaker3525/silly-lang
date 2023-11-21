

# f(x,y,z) = x + 1 * 3 * y * z + a -> {f:closure([x, y, z], expr(x + 1 * 3 * y * z + a))}

class Closure:
    def __init__(self, ids:list[str], e, env:"Env"):
        self.ids:list[str] = ids
        self.e = e
        self.env:"Env" = env
    def bind(self, es:list):
        d = {self.ids[i]: es[i] for i in range(len(es))}
        return self.env.ext(Env(d))

class Env:
    def __init__(self, binds:dict[str, (int|Closure)]):
        self.binds = binds
    def __str__(self):
        return str(self.binds)
    def __len__(self):
        return len(self.binds)
    def lookup(self, ids:str):
        return self.binds[ids]
    def ext(self, env:"Env"):
        binds = dict(self.binds)
        for xid, e in env.binds.items():
            binds[xid] = e
        return Env(binds)

class CEnv:
    def __init__(self, stack:list[int]):
        self.stack = stack
    def __str__(self):
        return str(self.stack)
    def __len__(self):
        return len(self.stack)
    def lookup(self, xid:str):
        for i, sid in enumerate(self.stack):
            if sid == xid:
                return len(self.stack) - i - 1
    def add_offset(self, n:int, ph=None):
        stack = list(self.stack)
        for i in range(abs(n)):
            stack.append(ph)
        #print(stack)
        return CEnv(stack)
            
    def ext(self, env:"CEnv"):
        stack = list(self.stack)
        for xid in env.stack:
            stack.append(xid)
        return CEnv(stack)