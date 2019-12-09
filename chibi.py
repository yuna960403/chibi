import pegpy
#from pegpy.tpeg import ParseTree
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)

'''
tree = parser('1+2*3')
print(repr(tree))
tree = parser('1@2*3')
print(repr(tree))
'''

class Expr(object):
    @classmethod
    def new(cls, v):
        if isinstance(v, Expr):
            return v
        return Val(v)

class Val(Expr):
    __slots__ = ['value']
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Val({self.value})'
    def eval(self, env: dict):
        return self.value
e = Val(0)
assert e.eval({}) == 0

class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left},{self.right})'

class Add(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) + self.right.eval(env)

class Sub(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) - self.right.eval(env)

class Mul(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      
        return self.left.eval(env) * self.right.eval(env)

class Div(Binary):
    __slots__ = ['left', 'right'] 
    def eval(self, env: dict):      
        return self.left.eval(env) // self.right.eval(env)

class Mod(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) % self.right.eval(env)

class Eq(Binary):   #left == right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond == x:y
        return 1 if self.left.eval(env) == self.right.eval(env) else 0   #1 if ~ else 0:真の値を1、偽の値を0とする

class Ne(Binary):   #left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond != x:y
        return 1 if self.left.eval(env) != self.right.eval(env) else 0

class Lt(Binary):   #left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond < x:y
        return 1 if self.left.eval(env) < self.right.eval(env) else 0

class Lte(Binary):   #left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond <= x:y
        return 1 if self.left.eval(env) <= self.right.eval(env) else 0

class Gt(Binary):   #left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond > x:y
        return 1 if self.left.eval(env) > self.right.eval(env) else 0

class Gte(Binary):   #left != right
    __slots__ = ['left', 'right']
    def eval(self, env: dict):      #cond >= x:y
        return 1 if self.left.eval(env) >= self.right.eval(env) else 0

class Var(Expr):
    __slots__ = ['name']

    def __init__(self,name):
        self.name = name

    def eval(self,env:dict):
        if self.name in env:
            return env[self.name]
        raise NameError(self.name)

class Assign(Expr):
    __slots__ = ['name','e']
    def __init__(self,name,e):
        self.name = name
        self.e = Expr.new(e)
    
    def eval(self,env):
        env[self.name] = self.e.eval(env)
        return env[self.name]

class Block(Expr):
    __slots__ = ['exprs']
    def __init__(self,*exprs):     #可変長の個の引数
        self.exprs = exprs      #[e,e2,e3,e4,e5]リストになっている

    def eval(self,env):
        for e in self.exprs:
            e.eval(env)

class While(Expr):
    __slots__ = ['cond','body']
    def __init__(self,cond,body):
        self.cond = cond
        self.body = body

    def eval(self,env):
        while self.cond.eval(env) != 0:
            self.body.eval(env)

class If(Expr):
    __slots__ = ['cond','then','else_']
    def __init__(self,cond,then,else_):
        self.cond = cond
        self.then = then
        self.else_ = else_

    def eval(self,env):
        yesorno = self.cond.eval(env)
        if yesorno == 1:
            return self.then.eval(env)
        else:
            return self.else_.eval(env)

e = Block(
    Assign('x',Val(1)),
    Assign('y',Val(2)),
    If(Gt(Var('x'),Var('y')),Var('x'),Var('y'))
)
assert e.eval ({}) == 2

def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
    if tree == 'If':
        return If(conv(tree[0]),conv(tree[1]),conv(tree[2]))
    if tree == 'While':
        return While(conv(tree[0]),conv(tree[1]))
    if tree == 'Val' or tree == 'Int':
        return Val(int(str(tree)))
    if tree == 'Add':
        return Add(conv(tree[0]), conv(tree[1]))
    if tree == 'Sub':
        return Sub(conv(tree[0]), conv(tree[1]))
    if tree == 'Mul':
        return Mul(conv(tree[0]), conv(tree[1]))
    if tree == 'Div':
        return Div(conv(tree[0]), conv(tree[1]))
    if tree == 'Mod':
        return Mod(conv(tree[0]), conv(tree[1]))
    if tree == 'Eq':
        return Eq(conv(tree[0]), conv(tree[1]))
    if tree == 'Ne':
        return Ne(conv(tree[0]), conv(tree[1]))
    if tree == 'Lt':
        return Lt(conv(tree[0]), conv(tree[1]))
    if tree == 'Lte':
        return Lte(conv(tree[0]), conv(tree[1]))
    if tree == 'Gt':
        return Gt(conv(tree[0]), conv(tree[1]))
    if tree == 'Gte':
        return Gte(conv(tree[0]), conv(tree[1]))
    if tree == 'Var':
        return Var(str(tree))
    if tree == 'LetDecl':
        return Assign(str(tree[0]), conv(tree[1]))
    print('@TODO', tree.tag,repr(tree))
    return Val(str(tree))

def run(src: str,env:dict):
    tree = parser(src)
    if tree.isError():
        print(repr(tree))
    else:
        e = conv(tree)
        print('env',env)
        print(e.eval(env))

def main():
    try:
        env = {}
        while True:
            s = input('>>> ')
            if s == '':
                break
            run(s,env)
    except EOFError:
        return
if __name__ == '__main__':
    main()











