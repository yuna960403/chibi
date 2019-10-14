
class Expr(object):
    pass

class Val(Expr):
    __slots__ = ['value']
    def __init__(self,value = 0):
        self.value = value
    def __repr__(self):
        return f'Val({self.value})'
    def eval(self):
        return self.value

v = Val(1)
assert v.eval() == 1
print(v)

assert isinstance(v,Expr)   # ==> True
assert isinstance(v,Val)    # ==> True
assert not isinstance(v,int)    # ==> notを入れることでTrueになる=>実行可能になる

def toExpr(a):
    if not isinstance(a,Expr):
            a = Val(a)
    return a

class Add(Expr):
    __slots__ = ['left','right']
    def __init__(self,a,b):
        self.left = toExpr(a)       #aとbは式
        self.right = toExpr(b) 
    def eval(self):
        return self.left.eval() + self.right.eval()

class Binary(object):
    __slots__ = ['left','right']
    def __init__(self):             #未完成
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname},{self.left},{self.right}'

e = Add(Val(1),Val(2))        #1+2
assert e.eval() == 3

#次のステップ 1+2+3 ==> 6

e = Add(Val(1),Add(Val(2),Val(3)))
assert e.eval() == 6
