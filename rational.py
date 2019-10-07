class Q(object):
    def __init__(self,a,b=1):       #b=1で分母を無効化できる
        self.a = a
        self.b = b
    def __repr__(self):
        if self.b == 1:             #分母を消す
            return str(self.a)
        return f'{self.a}/{self.b}'

q = Q(3)
print(q)